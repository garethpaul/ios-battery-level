//
//  ViewController.swift
//  ChargeMe
//
//  Created by Gareth on 5/23/15.
//  Copyright (c) 2015 GarethPaul. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()

        _ = self.readBatteryLevel()

        // Do any additional setup after loading the view, typically from a nib.
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
