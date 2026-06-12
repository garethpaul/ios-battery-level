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

    override func viewDidLoad() {
        super.viewDidLoad()

        configureBatteryLevelLabel()
        displayBatteryLevel(readBatteryLevel())

        // Do any additional setup after loading the view, typically from a nib.
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
        let wasBatteryMonitoringEnabled = device.isBatteryMonitoringEnabled
        device.isBatteryMonitoringEnabled = true
        defer {
            device.isBatteryMonitoringEnabled = wasBatteryMonitoringEnabled
        }

        let batteryLevel = device.batteryLevel
        return normalizedBatteryLevel(batteryLevel)
    }

    func displayBatteryLevel(_ batteryLevel: Float?) {
        batteryLevelLabel.text = batteryLevelText(batteryLevel)
        batteryLevelLabel.accessibilityValue = batteryLevelAccessibilityValue(batteryLevel)
    }

    func batteryLevelText(_ batteryLevel: Float?) -> String {
        guard let batteryLevel = batteryLevel,
              let normalizedLevel = normalizedBatteryLevel(batteryLevel) else {
            return "Battery Level: Unknown"
        }

        return String(format: "Battery Level: %.0f%%", Double(normalizedLevel * 100.0))
    }

    func batteryLevelAccessibilityValue(_ batteryLevel: Float?) -> String {
        guard let batteryLevel = batteryLevel,
              let normalizedLevel = normalizedBatteryLevel(batteryLevel) else {
            return "Unknown"
        }

        return String(format: "%.0f%%", Double(normalizedLevel * 100.0))
    }

    func normalizedBatteryLevel(_ batteryLevel: Float) -> Float? {
        if !(batteryLevel >= 0.0 && batteryLevel <= 1.0) {
            return nil
        }

        return batteryLevel
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}
