#!/usr/bin/env python3
from pathlib import Path
import plistlib
import re
import shutil
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BASELINE_PLAN = ROOT / "docs/plans/2026-06-08-ios-battery-baseline.md"
LIFECYCLE_PLAN = ROOT / "docs/plans/2026-06-08-battery-monitoring-lifecycle.md"
DEFER_PLAN = ROOT / "docs/plans/2026-06-08-battery-monitoring-defer.md"
UNKNOWN_LEVEL_PLAN = ROOT / "docs/plans/2026-06-08-unknown-battery-level.md"


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def strip_swift_line_comments(text):
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def require_order(text, tokens, message, failures):
    position = -1
    for token in tokens:
        next_position = text.find(token, position + 1)
        if next_position == -1:
            failures.append(message)
            return
        position = next_position


def parse_xml(relative_path, failures):
    try:
        ET.parse(str(ROOT / relative_path))
    except ET.ParseError as error:
        failures.append(f"{relative_path} is not well-formed XML: {error}")


def parse_plist(relative_path, failures):
    try:
        with (ROOT / relative_path).open("rb") as file:
            return plistlib.load(file)
    except Exception as error:
        failures.append(f"{relative_path} is not a readable plist: {error}")
        return {}


def main():
    failures = []
    required_files = [
        ".gitignore",
        "CHANGES.md",
        "Makefile",
        "README.md",
        "SECURITY.md",
        "VISION.md",
        "ChargeMe.xcodeproj/project.pbxproj",
        "ChargeMe.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
        "ChargeMe/Info.plist",
        "ChargeMe/AppDelegate.swift",
        "ChargeMe/ViewController.swift",
        "ChargeMeTests/ChargeMeTests.swift",
        "ChargeMeTests/Info.plist",
        "docs/plans/2026-06-08-ios-battery-baseline.md",
        "docs/plans/2026-06-08-battery-monitoring-lifecycle.md",
        "docs/plans/2026-06-08-battery-monitoring-defer.md",
        "docs/plans/2026-06-08-unknown-battery-level.md",
        "docs/readme-overview.svg",
    ]

    for relative_path in required_files:
        require((ROOT / relative_path).is_file(), f"Required file missing: {relative_path}", failures)

    for xml_file in [
        "ChargeMe.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
        "ChargeMe/Base.lproj/Main.storyboard",
        "ChargeMe/Base.lproj/LaunchScreen.xib",
        "docs/readme-overview.svg",
    ]:
        parse_xml(xml_file, failures)

    app_plist = parse_plist("ChargeMe/Info.plist", failures)
    test_plist = parse_plist("ChargeMeTests/Info.plist", failures)
    project = read("ChargeMe.xcodeproj/project.pbxproj")
    view_controller = read("ChargeMe/ViewController.swift")
    tests = read("ChargeMeTests/ChargeMeTests.swift")
    active_sources = "\n".join([
        strip_swift_line_comments(read("ChargeMe/AppDelegate.swift")),
        strip_swift_line_comments(view_controller),
        strip_swift_line_comments(tests),
    ])
    readme = read("README.md")
    vision = read("VISION.md")
    security = read("SECURITY.md")
    changes = read("CHANGES.md")
    gitignore = read(".gitignore")
    baseline_plan = BASELINE_PLAN.read_text(encoding="utf-8") if BASELINE_PLAN.exists() else ""
    lifecycle_plan = LIFECYCLE_PLAN.read_text(encoding="utf-8") if LIFECYCLE_PLAN.exists() else ""
    defer_plan = DEFER_PLAN.read_text(encoding="utf-8") if DEFER_PLAN.exists() else ""
    unknown_level_plan = UNKNOWN_LEVEL_PLAN.read_text(encoding="utf-8") if UNKNOWN_LEVEL_PLAN.exists() else ""

    require(app_plist.get("CFBundleIdentifier", "").startswith("com.garethpaul."),
            "ChargeMe Info.plist must keep the expected sample bundle identifier",
            failures)
    require(test_plist.get("CFBundlePackageType") == "BNDL",
            "ChargeMeTests Info.plist must remain a test bundle plist",
            failures)
    require("IPHONEOS_DEPLOYMENT_TARGET = 8.3;" in project and "INFOPLIST_FILE = ChargeMe/Info.plist;" in project,
            "Xcode project must preserve the legacy iOS deployment and plist wiring",
            failures)
    require("ENABLE_TESTABILITY = YES;" in project and "@testable import ChargeMe" in tests,
            "Xcode project and tests must keep ChargeMe app code testable from XCTest",
            failures)
    require("Pods" not in project and not (ROOT / "Podfile").exists(),
            "Battery sample must stay dependency-free unless dependencies are explicitly documented",
            failures)

    require("UIDevice.currentDevice()" in view_controller and ".batteryLevel" in view_controller,
            "ViewController must retain the UIDevice battery-level sample",
            failures)
    require("batteryMonitoringEnabled = true" in view_controller,
            "ViewController must enable battery monitoring before reading batteryLevel",
            failures)
    require("func readBatteryLevel() -> Float?" in view_controller and "_ = self.readBatteryLevel()" in view_controller,
            "ViewController must keep battery reads in an explicit optional helper invoked from viewDidLoad",
            failures)
    require("func normalizedBatteryLevel(batteryLevel: Float) -> Float?" in view_controller and
            "if batteryLevel < 0.0" in view_controller and "return nil" in view_controller,
            "ViewController must normalize unknown negative battery levels to nil",
            failures)
    require_order(
        view_controller,
        [
            "let wasBatteryMonitoringEnabled = device.batteryMonitoringEnabled",
            "device.batteryMonitoringEnabled = true",
            "defer {",
            "device.batteryMonitoringEnabled = wasBatteryMonitoringEnabled",
            "let batteryLevel = device.batteryLevel",
            "return normalizedBatteryLevel(batteryLevel)",
        ],
        "ViewController must restore batteryMonitoringEnabled with defer before returning the normalized battery level",
        failures,
    )
    require("testUnknownBatteryLevelReturnsNil" in tests and "XCTAssertNil" in tests and
            "testKnownBatteryLevelIsPreserved" in tests and "XCTAssertEqual" in tests and
            "XCTAssert(true" not in tests and "testPerformanceExample" not in tests,
            "ChargeMeTests must replace template tests with battery-level normalization assertions",
            failures)
    require(not re.search(r"\b(?:print|println|NSLog)\s*\(", active_sources),
            "Battery/device state must not be logged",
            failures)
    for forbidden in ["NSURL", "URLSession", "NSURLConnection", "http://", "https://", "upload", "analytics"]:
        require(forbidden not in active_sources,
                f"Battery sample must not add network, upload, or analytics behavior: {forbidden}",
                failures)

    swift_files = sorted((ROOT / "ChargeMe").rglob("*.swift")) + sorted((ROOT / "ChargeMeTests").rglob("*.swift"))
    require(len(swift_files) >= 3,
            "expected Swift source/test inventory is missing",
            failures)
    require("*.local.xcconfig" in gitignore and ".env" in gitignore and "DerivedData" in gitignore,
            ".gitignore must exclude local config and Xcode build products",
            failures)
    require("make check" in readme and "ChargeMe.xcodeproj" in readme and "batteryMonitoringEnabled" in readme and
            "restore" in readme.lower() and "defer" in readme.lower() and "unknown" in readme.lower(),
            "README must document static verification, project usage, and deferred battery monitoring restoration",
            failures)
    require("local-only" in readme.lower() and "battery" in readme.lower(),
            "README must document local-only battery data expectations",
            failures)
    require("scripts/check-baseline.py" in vision and "local-only" in vision.lower() and
            "defer" in vision.lower() and "unknown" in vision.lower(),
            "VISION must describe the current static privacy baseline",
            failures)
    require("battery" in security.lower() and "make check" in security and "unknown" in security.lower(),
            "SECURITY must document battery/device-state privacy and the static baseline",
            failures)
    require("battery monitoring" in changes.lower() and "make check" in changes and "restores" in changes and
            "defer" in changes.lower() and "unknown" in changes.lower(),
            "CHANGES must record the battery monitoring fix, unknown-level normalization, deferred restoration, and baseline",
            failures)
    require("status: completed" in baseline_plan and "status: completed" in lifecycle_plan and
            "status: completed" in defer_plan and "status: completed" in unknown_level_plan,
            "plans must be marked completed",
            failures)

    if shutil.which("xcodebuild"):
        print("xcodebuild is available; run a scheme-specific Xcode test on macOS before release.")
    else:
        print("xcodebuild unavailable; static iOS baseline only.")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("ios-battery-level baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
