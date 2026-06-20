//
//  ViewController.swift
//  ChargeMe
//
//  Created by Gareth on 5/23/15.
//  Copyright (c) 2015 GarethPaul. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    let batteryLevelLabel = UILabel()
    private var batteryLevelObserver: NSObjectProtocol?
    private var applicationDidBecomeActiveObserver: NSObjectProtocol?
    private var observedNotificationCenter: NotificationCenter?
    private var wasBatteryMonitoringEnabled: Bool?
    private var batteryUpdateGeneration = 0

    override func viewDidLoad() {
        super.viewDidLoad()

        configureBatteryLevelLabel()

        // Do any additional setup after loading the view, typically from a nib.
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        startBatteryLevelUpdates()
    }

    override func viewDidDisappear(_ animated: Bool) {
        stopBatteryLevelUpdates()
        super.viewDidDisappear(animated)
    }

    deinit {
        stopBatteryLevelUpdates()
    }

    private func startBatteryLevelUpdates() {
        if batteryLevelObserver == nil {
            batteryUpdateGeneration += 1
            let updateGeneration = batteryUpdateGeneration
            let center = notificationCenter()
            observedNotificationCenter = center
            wasBatteryMonitoringEnabled = batteryMonitoringEnabled()
            setBatteryMonitoringEnabled(true)
            batteryLevelObserver = center.addObserver(
                forName: UIDevice.batteryLevelDidChangeNotification,
                object: batteryNotificationObject(),
                queue: batteryNotificationQueue()
            ) { [weak self] _ in
                self?.refreshBatteryLevel(for: updateGeneration)
            }
            applicationDidBecomeActiveObserver = center.addObserver(
                forName: UIApplication.didBecomeActiveNotification,
                object: nil,
                queue: batteryNotificationQueue()
            ) { [weak self] _ in
                self?.refreshBatteryLevel(for: updateGeneration)
            }
        }

        displayBatteryLevel(readBatteryLevel())
    }

    private func stopBatteryLevelUpdates() {
        batteryUpdateGeneration += 1

        if let center = observedNotificationCenter {
            if let observer = batteryLevelObserver {
                center.removeObserver(observer)
            }
            if let observer = applicationDidBecomeActiveObserver {
                center.removeObserver(observer)
            }
        }

        batteryLevelObserver = nil
        applicationDidBecomeActiveObserver = nil
        observedNotificationCenter = nil

        if let previousMonitoringState = wasBatteryMonitoringEnabled {
            setBatteryMonitoringEnabled(previousMonitoringState)
            wasBatteryMonitoringEnabled = nil
        }
    }

    func isBatteryUpdateGenerationActive(_ generation: Int) -> Bool {
        return batteryLevelObserver != nil &&
            applicationDidBecomeActiveObserver != nil &&
            generation == batteryUpdateGeneration
    }

    func refreshBatteryLevel(for generation: Int) {
        guard isBatteryUpdateGenerationActive(generation) else {
            return
        }

        displayBatteryLevel(readBatteryLevel())
    }

    func batteryMonitoringEnabled() -> Bool {
        return UIDevice.current.isBatteryMonitoringEnabled
    }

    func setBatteryMonitoringEnabled(_ enabled: Bool) {
        UIDevice.current.isBatteryMonitoringEnabled = enabled
    }

    func notificationCenter() -> NotificationCenter {
        return NotificationCenter.default
    }

    func batteryNotificationObject() -> Any? {
        return UIDevice.current
    }

    func batteryNotificationQueue() -> OperationQueue? {
        return OperationQueue.main
    }

    func configureBatteryLevelLabel() {
        batteryLevelLabel.textAlignment = .center
        batteryLevelLabel.accessibilityLabel = "Battery Level"
        batteryLevelLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(batteryLevelLabel)
        view.addConstraints([
            NSLayoutConstraint(item: batteryLevelLabel, attribute: .centerX, relatedBy: .equal, toItem: view, attribute: .centerX, multiplier: 1.0, constant: 0.0),
            NSLayoutConstraint(item: batteryLevelLabel, attribute: .centerY, relatedBy: .equal, toItem: view, attribute: .centerY, multiplier: 1.0, constant: 0.0)
        ])
    }

    func readBatteryLevel() -> Float? {
        let device = UIDevice.current
        let wasBatteryMonitoringEnabled = batteryMonitoringEnabled()
        setBatteryMonitoringEnabled(true)
        defer {
            setBatteryMonitoringEnabled(wasBatteryMonitoringEnabled)
        }

        let batteryLevel = device.batteryLevel
        return normalizedBatteryLevel(batteryLevel)
    }

    func displayBatteryLevel(_ batteryLevel: Float?) {
        batteryLevelLabel.text = batteryLevelText(batteryLevel)
        batteryLevelLabel.accessibilityValue = batteryLevelAccessibilityValue(batteryLevel)
    }

    func batteryLevelText(_ batteryLevel: Float?) -> String {
        guard let percentage = batteryPercentage(batteryLevel) else {
            return "Battery Level: Unknown"
        }

        return "Battery Level: \(percentage)%"
    }

    func batteryLevelAccessibilityValue(_ batteryLevel: Float?) -> String {
        guard let percentage = batteryPercentage(batteryLevel) else {
            return "Unknown"
        }

        return "\(percentage)%"
    }

    func batteryPercentage(_ batteryLevel: Float?) -> Int? {
        guard let batteryLevel = batteryLevel,
              let normalizedLevel = normalizedBatteryLevel(batteryLevel) else {
            return nil
        }

        return Int((Double(normalizedLevel) * 100.0).rounded(.toNearestOrAwayFromZero))
    }

    func normalizedBatteryLevel(_ batteryLevel: Float) -> Float? {
        if !batteryLevel.isFinite || !(batteryLevel >= 0.0 && batteryLevel <= 1.0) {
            return nil
        }

        return batteryLevel
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}
