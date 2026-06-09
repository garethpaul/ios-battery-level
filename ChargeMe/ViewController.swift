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
        displayBatteryLevel(self.readBatteryLevel())

        // Do any additional setup after loading the view, typically from a nib.
    }

    func configureBatteryLevelLabel() {
        batteryLevelLabel.textAlignment = .Center
        batteryLevelLabel.accessibilityLabel = "Battery Level"
        batteryLevelLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(batteryLevelLabel)
        view.addConstraints([
            NSLayoutConstraint(item: batteryLevelLabel, attribute: .CenterX, relatedBy: .Equal, toItem: view, attribute: .CenterX, multiplier: 1.0, constant: 0.0),
            NSLayoutConstraint(item: batteryLevelLabel, attribute: .CenterY, relatedBy: .Equal, toItem: view, attribute: .CenterY, multiplier: 1.0, constant: 0.0)
        ])
    }

    func readBatteryLevel() -> Float? {
        let device = UIDevice.currentDevice()
        let wasBatteryMonitoringEnabled = device.batteryMonitoringEnabled
        device.batteryMonitoringEnabled = true
        defer {
            device.batteryMonitoringEnabled = wasBatteryMonitoringEnabled
        }

        let batteryLevel = device.batteryLevel
        return normalizedBatteryLevel(batteryLevel)
    }

    func displayBatteryLevel(batteryLevel: Float?) {
        batteryLevelLabel.text = batteryLevelText(batteryLevel)
    }

    func batteryLevelText(batteryLevel: Float?) -> String {
        guard let batteryLevel = batteryLevel else {
            return "Battery Level: Unknown"
        }

        return String(format: "Battery Level: %.0f%%", Double(batteryLevel * 100.0))
    }

    func normalizedBatteryLevel(batteryLevel: Float) -> Float? {
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
