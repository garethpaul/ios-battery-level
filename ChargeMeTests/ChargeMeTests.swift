//
//  ChargeMeTests.swift
//  ChargeMeTests
//
//  Created by Gareth on 5/23/15.
//  Copyright (c) 2015 GarethPaul. All rights reserved.
//

import UIKit
import XCTest
@testable import ChargeMe

private final class BatteryProbe {
    var level: Float?
    var monitoringEnabled = false
    var readCount = 0
}

private final class StubBatteryViewController: ViewController {
    let probe: BatteryProbe
    let center: NotificationCenter
    let notificationObject = NSObject()

    init(probe: BatteryProbe = BatteryProbe(), center: NotificationCenter = NotificationCenter()) {
        self.probe = probe
        self.center = center
        super.init(nibName: nil, bundle: nil)
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    override func readBatteryLevel() -> Float? {
        probe.readCount += 1
        return probe.level
    }

    override func batteryMonitoringEnabled() -> Bool {
        return probe.monitoringEnabled
    }

    override func setBatteryMonitoringEnabled(_ enabled: Bool) {
        probe.monitoringEnabled = enabled
    }

    override func notificationCenter() -> NotificationCenter {
        return center
    }

    override func batteryNotificationObject() -> Any? {
        return notificationObject
    }

    override func batteryNotificationQueue() -> OperationQueue? {
        return nil
    }
}

class ChargeMeTests: XCTestCase {

    func testViewAppearanceRefreshesVisibleAndAccessibleBatteryLevel() {
        let controller = StubBatteryViewController()
        controller.probe.level = 0.25
        controller.loadViewIfNeeded()

        XCTAssertEqual(controller.probe.readCount, 0, "View loading should only configure the label")

        controller.viewWillAppear(false)
        XCTAssertEqual(controller.batteryLevelLabel.text, "Battery Level: 25%")
        XCTAssertEqual(controller.batteryLevelLabel.accessibilityValue, "25%")

        controller.probe.level = 0.75
        controller.viewWillAppear(false)
        XCTAssertEqual(controller.probe.readCount, 2)
        XCTAssertEqual(controller.batteryLevelLabel.text, "Battery Level: 75%")
        XCTAssertEqual(controller.batteryLevelLabel.accessibilityValue, "75%")
    }

    func testBatteryNotificationRefreshesOnceWhileVisibleAndStopsAfterDisappearance() {
        let controller = StubBatteryViewController()
        controller.probe.level = 0.25
        controller.loadViewIfNeeded()
        controller.viewWillAppear(false)
        controller.viewWillAppear(false)

        controller.probe.level = 0.75
        controller.center.post(
            name: UIDevice.batteryLevelDidChangeNotification,
            object: controller.notificationObject
        )

        XCTAssertEqual(controller.probe.readCount, 3, "Repeated appearances must retain one battery observer")
        XCTAssertEqual(controller.batteryLevelLabel.text, "Battery Level: 75%")
        XCTAssertEqual(controller.batteryLevelLabel.accessibilityValue, "75%")

        controller.viewDidDisappear(false)
        controller.probe.level = 0.5
        controller.center.post(
            name: UIDevice.batteryLevelDidChangeNotification,
            object: controller.notificationObject
        )

        XCTAssertEqual(controller.probe.readCount, 3, "Hidden views must stop receiving battery notifications")
        XCTAssertEqual(controller.batteryLevelLabel.text, "Battery Level: 75%")
        XCTAssertEqual(controller.batteryLevelLabel.accessibilityValue, "75%")
    }

    func testBatteryMonitoringIsEnabledOnlyWhileVisible() {
        let controller = StubBatteryViewController()
        controller.probe.level = 0.5
        controller.loadViewIfNeeded()
        controller.viewWillAppear(false)
        XCTAssertTrue(controller.probe.monitoringEnabled)

        controller.viewDidDisappear(false)
        XCTAssertFalse(controller.probe.monitoringEnabled)
    }

    func testBatteryMonitoringRestoresPreviouslyEnabledState() {
        let probe = BatteryProbe()
        probe.level = 0.5
        probe.monitoringEnabled = true
        let controller = StubBatteryViewController(probe: probe)
        controller.loadViewIfNeeded()

        controller.viewWillAppear(false)
        controller.viewDidDisappear(false)

        XCTAssertTrue(probe.monitoringEnabled)
    }

    func testVisibleControllerRefreshesWhenApplicationBecomesActive() {
        let controller = StubBatteryViewController()
        controller.probe.level = 0.25
        controller.loadViewIfNeeded()
        controller.viewWillAppear(false)

        controller.probe.level = 0.75
        controller.center.post(name: UIApplication.didBecomeActiveNotification, object: nil)

        XCTAssertEqual(controller.probe.readCount, 2)
        XCTAssertEqual(controller.batteryLevelLabel.text, "Battery Level: 75%")
        XCTAssertEqual(controller.batteryLevelLabel.accessibilityValue, "75%")
    }

    func testBatteryNotificationIgnoresUnrelatedObjects() {
        let controller = StubBatteryViewController()
        controller.probe.level = 0.25
        controller.loadViewIfNeeded()
        controller.viewWillAppear(false)

        controller.probe.level = 0.75
        controller.center.post(
            name: UIDevice.batteryLevelDidChangeNotification,
            object: NSObject()
        )

        XCTAssertEqual(controller.probe.readCount, 1)
        XCTAssertEqual(controller.batteryLevelLabel.text, "Battery Level: 25%")
    }

    func testControllerDeinitRemovesObserversAndRestoresMonitoring() {
        let probe = BatteryProbe()
        probe.level = 0.25
        let center = NotificationCenter()
        var notificationObject: NSObject!
        weak var weakController: StubBatteryViewController?

        autoreleasepool {
            var controller: StubBatteryViewController? = StubBatteryViewController(probe: probe, center: center)
            notificationObject = controller!.notificationObject
            controller!.loadViewIfNeeded()
            controller!.viewWillAppear(false)
            weakController = controller
            controller = nil
        }

        XCTAssertNil(weakController)
        XCTAssertFalse(probe.monitoringEnabled)
        center.post(name: UIDevice.batteryLevelDidChangeNotification, object: notificationObject)
        center.post(name: UIApplication.didBecomeActiveNotification, object: nil)
        XCTAssertEqual(probe.readCount, 1)
    }

    func testStaleBatteryNotificationGenerationCannotRefreshLaterLifecycle() {
        let controller = StubBatteryViewController()
        controller.probe.level = 0.25
        controller.loadViewIfNeeded()
        controller.viewWillAppear(false)

        XCTAssertTrue(controller.isBatteryUpdateGenerationActive(1))
        controller.viewDidDisappear(false)
        XCTAssertFalse(controller.isBatteryUpdateGenerationActive(1))

        controller.probe.level = 0.75
        controller.viewWillAppear(false)
        XCTAssertTrue(controller.isBatteryUpdateGenerationActive(3))
        XCTAssertEqual(controller.probe.readCount, 2)

        controller.refreshBatteryLevel(for: 1)
        XCTAssertEqual(controller.probe.readCount, 2, "A stale queued callback must not refresh a later lifecycle")

        controller.refreshBatteryLevel(for: 3)
        XCTAssertEqual(controller.probe.readCount, 3)
        XCTAssertEqual(controller.batteryLevelLabel.text, "Battery Level: 75%")
        XCTAssertEqual(controller.batteryLevelLabel.accessibilityValue, "75%")
    }

    func testUnknownBatteryLevelReturnsNil() {
        let controller = ViewController()
        XCTAssertNil(controller.normalizedBatteryLevel(-1.0), "Unknown battery levels should not be treated as percentages")
    }

    func testKnownBatteryLevelIsPreserved() {
        let controller = ViewController()
        XCTAssertEqual(controller.normalizedBatteryLevel(0.75)!, 0.75, "Known battery levels should be preserved")
    }

    func testZeroBatteryLevelIsPreserved() {
        let controller = ViewController()
        XCTAssertEqual(controller.normalizedBatteryLevel(0.0)!, 0.0, "An empty battery should remain a valid percentage")
    }

    func testFullBatteryLevelIsPreserved() {
        let controller = ViewController()
        XCTAssertEqual(controller.normalizedBatteryLevel(1.0)!, 1.0, "A full battery should remain a valid percentage")
    }

    func testOutOfRangeBatteryLevelReturnsNil() {
        let controller = ViewController()
        XCTAssertNil(controller.normalizedBatteryLevel(1.5), "Battery levels above 100% should not be treated as percentages")
    }

    func testNaNBatteryLevelReturnsNil() {
        let controller = ViewController()
        let notANumber = Float(0.0) / Float(0.0)
        XCTAssertNil(controller.normalizedBatteryLevel(notANumber), "Non-finite battery levels should not be treated as percentages")
    }

    func testBatteryLevelTextShowsKnownPercentage() {
        let controller = ViewController()
        XCTAssertEqual(controller.batteryLevelText(0.75), "Battery Level: 75%", "Known battery levels should be formatted as percentages")
    }

    func testBatteryLevelTextShowsZeroPercentage() {
        let controller = ViewController()
        XCTAssertEqual(controller.batteryLevelText(0.0), "Battery Level: 0%", "Zero battery level should be shown as a valid percentage")
    }

    func testBatteryLevelTextShowsUnknownWhenMissing() {
        let controller = ViewController()
        XCTAssertEqual(controller.batteryLevelText(nil), "Battery Level: Unknown", "Unknown battery levels should be visible without inventing a percentage")
    }

    func testBatteryLevelTextShowsUnknownForInvalidValues() {
        let controller = ViewController()
        XCTAssertEqual(controller.batteryLevelText(1.5), "Battery Level: Unknown")
        XCTAssertEqual(controller.batteryLevelText(Float.nan), "Battery Level: Unknown")
    }

    func testBatteryLevelAccessibilityValueShowsKnownPercentage() {
        let controller = ViewController()
        XCTAssertEqual(controller.batteryLevelAccessibilityValue(0.75), "75%", "Known battery levels should be exposed as accessibility values")
    }

    func testBatteryLevelAccessibilityValueShowsZeroPercentage() {
        let controller = ViewController()
        XCTAssertEqual(controller.batteryLevelAccessibilityValue(0.0), "0%", "Zero battery level should remain a valid accessibility value")
    }

    func testBatteryLevelAccessibilityValueShowsUnknownWhenMissing() {
        let controller = ViewController()
        XCTAssertEqual(controller.batteryLevelAccessibilityValue(nil), "Unknown", "Unknown battery levels should be exposed without inventing a percentage")
    }

    func testBatteryLevelAccessibilityValueShowsUnknownForInvalidValues() {
        let controller = ViewController()
        XCTAssertEqual(controller.batteryLevelAccessibilityValue(1.5), "Unknown")
        XCTAssertEqual(controller.batteryLevelAccessibilityValue(Float.nan), "Unknown")
    }

    func testBatteryPercentageRoundsHalfAwayFromZero() {
        let controller = ViewController()
        XCTAssertEqual(controller.batteryLevelText(0.0049), "Battery Level: 0%")
        XCTAssertEqual(controller.batteryLevelText(0.125), "Battery Level: 13%")
        XCTAssertEqual(controller.batteryLevelAccessibilityValue(0.995), "100%")
    }

    func testInfiniteBatteryLevelsAreUnknown() {
        let controller = ViewController()
        XCTAssertNil(controller.normalizedBatteryLevel(Float.infinity))
        XCTAssertNil(controller.normalizedBatteryLevel(-Float.infinity))
    }

}
