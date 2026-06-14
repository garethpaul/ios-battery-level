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

private final class StubBatteryViewController: ViewController {
    var stubbedBatteryLevel: Float?
    var batteryReadCount = 0

    override func readBatteryLevel() -> Float? {
        batteryReadCount += 1
        return stubbedBatteryLevel
    }
}

class ChargeMeTests: XCTestCase {

    func testViewAppearanceRefreshesVisibleAndAccessibleBatteryLevel() {
        let controller = StubBatteryViewController()
        controller.stubbedBatteryLevel = 0.25
        controller.loadViewIfNeeded()

        XCTAssertEqual(controller.batteryReadCount, 0, "View loading should only configure the label")

        controller.viewWillAppear(false)
        XCTAssertEqual(controller.batteryLevelLabel.text, "Battery Level: 25%")
        XCTAssertEqual(controller.batteryLevelLabel.accessibilityValue, "25%")

        controller.stubbedBatteryLevel = 0.75
        controller.viewWillAppear(false)
        XCTAssertEqual(controller.batteryReadCount, 2)
        XCTAssertEqual(controller.batteryLevelLabel.text, "Battery Level: 75%")
        XCTAssertEqual(controller.batteryLevelLabel.accessibilityValue, "75%")
    }

    func testBatteryNotificationRefreshesOnceWhileVisibleAndStopsAfterDisappearance() {
        let controller = StubBatteryViewController()
        controller.stubbedBatteryLevel = 0.25
        controller.loadViewIfNeeded()
        controller.viewWillAppear(false)
        controller.viewWillAppear(false)

        controller.stubbedBatteryLevel = 0.75
        NotificationCenter.default.post(
            name: UIDevice.batteryLevelDidChangeNotification,
            object: UIDevice.current
        )

        XCTAssertEqual(controller.batteryReadCount, 3, "Repeated appearances must retain one battery observer")
        XCTAssertEqual(controller.batteryLevelLabel.text, "Battery Level: 75%")
        XCTAssertEqual(controller.batteryLevelLabel.accessibilityValue, "75%")

        controller.viewDidDisappear(false)
        controller.stubbedBatteryLevel = 0.5
        NotificationCenter.default.post(
            name: UIDevice.batteryLevelDidChangeNotification,
            object: UIDevice.current
        )

        XCTAssertEqual(controller.batteryReadCount, 3, "Hidden views must stop receiving battery notifications")
        XCTAssertEqual(controller.batteryLevelLabel.text, "Battery Level: 75%")
        XCTAssertEqual(controller.batteryLevelLabel.accessibilityValue, "75%")
    }

    func testBatteryMonitoringIsEnabledOnlyWhileVisible() {
        let device = UIDevice.current
        let originalMonitoringState = device.isBatteryMonitoringEnabled
        device.isBatteryMonitoringEnabled = false
        defer {
            device.isBatteryMonitoringEnabled = originalMonitoringState
        }

        let controller = StubBatteryViewController()
        controller.stubbedBatteryLevel = 0.5
        controller.loadViewIfNeeded()
        controller.viewWillAppear(false)
        XCTAssertTrue(device.isBatteryMonitoringEnabled)

        controller.viewDidDisappear(false)
        XCTAssertFalse(device.isBatteryMonitoringEnabled)
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

}
