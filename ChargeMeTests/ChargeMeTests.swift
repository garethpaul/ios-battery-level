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

class ChargeMeTests: XCTestCase {

    func testUnknownBatteryLevelReturnsNil() {
        let controller = ViewController()
        XCTAssertNil(controller.normalizedBatteryLevel(-1.0), "Unknown battery levels should not be treated as percentages")
    }

    func testKnownBatteryLevelIsPreserved() {
        let controller = ViewController()
        XCTAssertEqual(controller.normalizedBatteryLevel(0.75)!, 0.75, "Known battery levels should be preserved")
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

}
