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

}
