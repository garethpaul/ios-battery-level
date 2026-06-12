#!/usr/bin/env python3
from pathlib import Path
import plistlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BASELINE_PLAN = ROOT / "docs/plans/2026-06-08-ios-battery-baseline.md"
MAKE_GATES_PLAN = ROOT / "docs/plans/2026-06-09-make-gate-aliases.md"
LIFECYCLE_PLAN = ROOT / "docs/plans/2026-06-08-battery-monitoring-lifecycle.md"
DEFER_PLAN = ROOT / "docs/plans/2026-06-08-battery-monitoring-defer.md"
UNKNOWN_LEVEL_PLAN = ROOT / "docs/plans/2026-06-08-unknown-battery-level.md"
UPPER_BOUND_PLAN = ROOT / "docs/plans/2026-06-09-battery-level-upper-bound.md"
NONFINITE_PLAN = ROOT / "docs/plans/2026-06-09-nonfinite-battery-level.md"
ZERO_LEVEL_PLAN = ROOT / "docs/plans/2026-06-09-zero-battery-level.md"
DISPLAY_PLAN = ROOT / "docs/plans/2026-06-09-visible-battery-level.md"
ACCESSIBILITY_VALUE_PLAN = ROOT / "docs/plans/2026-06-09-battery-accessibility-value.md"
CI_PLAN = ROOT / "docs/plans/2026-06-10-ci-baseline.md"
HOSTED_VALIDATION_PLAN = ROOT / "docs/plans/2026-06-10-hosted-project-validation.md"
SWIFT_5_BUILD_PLAN = ROOT / "docs/plans/2026-06-10-swift-5-app-build.md"


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
        ".github/workflows/check.yml",
        ".gitignore",
        ".github/workflows/check.yml",
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
        "docs/plans/2026-06-09-make-gate-aliases.md",
        "docs/plans/2026-06-08-battery-monitoring-lifecycle.md",
        "docs/plans/2026-06-08-battery-monitoring-defer.md",
        "docs/plans/2026-06-08-unknown-battery-level.md",
        "docs/plans/2026-06-09-battery-level-upper-bound.md",
        "docs/plans/2026-06-09-nonfinite-battery-level.md",
        "docs/plans/2026-06-09-zero-battery-level.md",
        "docs/plans/2026-06-09-visible-battery-level.md",
        "docs/plans/2026-06-09-battery-accessibility-value.md",
        "docs/plans/2026-06-10-ci-baseline.md",
        "docs/plans/2026-06-10-hosted-project-validation.md",
        "docs/plans/2026-06-10-swift-5-app-build.md",
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
    makefile = read("Makefile")
    baseline_plan = BASELINE_PLAN.read_text(encoding="utf-8") if BASELINE_PLAN.exists() else ""
    make_gates_plan = MAKE_GATES_PLAN.read_text(encoding="utf-8") if MAKE_GATES_PLAN.exists() else ""
    lifecycle_plan = LIFECYCLE_PLAN.read_text(encoding="utf-8") if LIFECYCLE_PLAN.exists() else ""
    defer_plan = DEFER_PLAN.read_text(encoding="utf-8") if DEFER_PLAN.exists() else ""
    unknown_level_plan = UNKNOWN_LEVEL_PLAN.read_text(encoding="utf-8") if UNKNOWN_LEVEL_PLAN.exists() else ""
    upper_bound_plan = UPPER_BOUND_PLAN.read_text(encoding="utf-8") if UPPER_BOUND_PLAN.exists() else ""
    nonfinite_plan = NONFINITE_PLAN.read_text(encoding="utf-8") if NONFINITE_PLAN.exists() else ""
    zero_level_plan = ZERO_LEVEL_PLAN.read_text(encoding="utf-8") if ZERO_LEVEL_PLAN.exists() else ""
    display_plan = DISPLAY_PLAN.read_text(encoding="utf-8") if DISPLAY_PLAN.exists() else ""
    accessibility_value_plan = ACCESSIBILITY_VALUE_PLAN.read_text(encoding="utf-8") if ACCESSIBILITY_VALUE_PLAN.exists() else ""
    ci_plan = CI_PLAN.read_text(encoding="utf-8") if CI_PLAN.exists() else ""
    hosted_validation_plan = HOSTED_VALIDATION_PLAN.read_text(encoding="utf-8") if HOSTED_VALIDATION_PLAN.exists() else ""
    swift_5_build_plan = SWIFT_5_BUILD_PLAN.read_text(encoding="utf-8") if SWIFT_5_BUILD_PLAN.exists() else ""
    workflow = read(".github/workflows/check.yml")

    require(app_plist.get("CFBundleIdentifier", "").startswith("com.garethpaul."),
            "ChargeMe Info.plist must keep the expected sample bundle identifier",
            failures)
    require(test_plist.get("CFBundlePackageType") == "BNDL",
            "ChargeMeTests Info.plist must remain a test bundle plist",
            failures)
    require(project.count("IPHONEOS_DEPLOYMENT_TARGET = 12.0;") == 2 and
            "IPHONEOS_DEPLOYMENT_TARGET = 8.3;" not in project and
            project.count("SWIFT_VERSION = 5.0;") == 4 and
            "INFOPLIST_FILE = ChargeMe/Info.plist;" in project,
            "Xcode project must use Swift 5 and iOS 12 while preserving plist wiring",
            failures)
    require("ENABLE_TESTABILITY = YES;" in project and "@testable import ChargeMe" in tests,
            "Xcode project and tests must keep ChargeMe app code testable from XCTest",
            failures)
    require("[UIApplication.LaunchOptionsKey: Any]?" in active_sources and
            "func application(_ application: UIApplication" in active_sources,
            "AppDelegate must use the Swift 5 launch-options signature",
            failures)
    require("Pods" not in project and not (ROOT / "Podfile").exists(),
            "Battery sample must stay dependency-free unless dependencies are explicitly documented",
            failures)

    require("UIDevice.current" in view_controller and "UIDevice.currentDevice()" not in view_controller and
            ".batteryLevel" in view_controller,
            "ViewController must retain the UIDevice battery-level sample",
            failures)
    require("isBatteryMonitoringEnabled = true" in view_controller,
            "ViewController must enable battery monitoring before reading batteryLevel",
            failures)
    require("func readBatteryLevel() -> Float?" in view_controller and "displayBatteryLevel(readBatteryLevel())" in view_controller,
            "ViewController must keep battery reads in an explicit optional helper displayed from viewDidLoad",
            failures)
    require("let batteryLevelLabel = UILabel()" in view_controller and
            "func configureBatteryLevelLabel()" in view_controller and
            "batteryLevelLabel.accessibilityLabel = \"Battery Level\"" in view_controller and
            "NSLayoutConstraint(item: batteryLevelLabel" in view_controller,
            "ViewController must expose a local visible battery-level label",
            failures)
    require("func displayBatteryLevel(_ batteryLevel: Float?)" in view_controller and
            "batteryLevelLabel.text = batteryLevelText(batteryLevel)" in view_controller and
            "batteryLevelLabel.accessibilityValue = batteryLevelAccessibilityValue(batteryLevel)" in view_controller,
            "ViewController must display battery readings through the formatter",
            failures)
    require("func batteryLevelText(_ batteryLevel: Float?) -> String" in view_controller and
            "Battery Level: Unknown" in view_controller and
            'String(format: "Battery Level: %.0f%%"' in view_controller,
            "ViewController must format known and unknown battery levels for display",
            failures)
    require("func batteryLevelAccessibilityValue(_ batteryLevel: Float?) -> String" in view_controller and
            'return "Unknown"' in view_controller and
            'String(format: "%.0f%%"' in view_controller,
            "ViewController must expose known and unknown battery levels as accessibility values",
            failures)
    require_order(
        view_controller,
        [
            "configureBatteryLevelLabel()",
            "displayBatteryLevel(readBatteryLevel())",
        ],
        "ViewController must configure the battery label before displaying the sampled value",
        failures,
    )
    require("func normalizedBatteryLevel(_ batteryLevel: Float) -> Float?" in view_controller and
            "!(batteryLevel >= 0.0 && batteryLevel <= 1.0)" in view_controller and "return nil" in view_controller,
            "ViewController must normalize unknown, non-finite, or out-of-range battery levels to nil",
            failures)
    require_order(
        view_controller,
        [
            "let wasBatteryMonitoringEnabled = device.isBatteryMonitoringEnabled",
            "device.isBatteryMonitoringEnabled = true",
            "defer {",
            "device.isBatteryMonitoringEnabled = wasBatteryMonitoringEnabled",
            "let batteryLevel = device.batteryLevel",
            "return normalizedBatteryLevel(batteryLevel)",
        ],
        "ViewController must restore batteryMonitoringEnabled with defer before returning the normalized battery level",
        failures,
    )
    require("testUnknownBatteryLevelReturnsNil" in tests and "XCTAssertNil" in tests and
            "testKnownBatteryLevelIsPreserved" in tests and "XCTAssertEqual" in tests and
            "testZeroBatteryLevelIsPreserved" in tests and "normalizedBatteryLevel(0.0)" in tests and
            "testFullBatteryLevelIsPreserved" in tests and
            "testOutOfRangeBatteryLevelReturnsNil" in tests and
            "testNaNBatteryLevelReturnsNil" in tests and
            "testBatteryLevelTextShowsKnownPercentage" in tests and
            "Battery Level: 75%" in tests and
            "testBatteryLevelTextShowsZeroPercentage" in tests and
            "Battery Level: 0%" in tests and
            "testBatteryLevelTextShowsUnknownWhenMissing" in tests and
            "Battery Level: Unknown" in tests and
            "testBatteryLevelAccessibilityValueShowsKnownPercentage" in tests and
            '"75%"' in tests and
            "testBatteryLevelAccessibilityValueShowsZeroPercentage" in tests and
            '"0%"' in tests and
            "testBatteryLevelAccessibilityValueShowsUnknownWhenMissing" in tests and
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
    require(".PHONY: build check lint test" in makefile and "lint test build: check" in makefile,
            "Makefile must expose lint, test, and build aliases for the local baseline",
            failures)
    require("make lint" in readme and "make test" in readme and "make build" in readme and "make check" in readme and "GitHub Actions" in readme and "ChargeMe.xcodeproj" in readme and "batteryMonitoringEnabled" in readme and
            "restore" in readme.lower() and "defer" in readme.lower() and "unknown" in readme.lower() and "out-of-range" in readme.lower() and "non-finite" in readme.lower() and "zero" in readme.lower(),
            "README must document static verification, project usage, and deferred battery monitoring restoration",
            failures)
    require("visible" in readme.lower() and "Battery Level: Unknown" in readme and "accessibility value" in readme.lower(),
            "README must document visible battery-level display behavior",
            failures)
    require("local-only" in readme.lower() and "battery" in readme.lower(),
            "README must document local-only battery data expectations",
            failures)
    require("scripts/check-baseline.py" in vision and "make lint" in vision and "make test" in vision and "make build" in vision and "GitHub Actions" in vision and "local-only" in vision.lower() and
            "defer" in vision.lower() and "unknown" in vision.lower() and "out-of-range" in vision.lower() and "non-finite" in vision.lower() and "zero" in vision.lower() and "visible" in vision.lower() and "accessibility value" in vision.lower(),
            "VISION must describe the current static privacy baseline",
            failures)
    require("battery" in security.lower() and "make check" in security and "GitHub Actions" in security and "unknown" in security.lower() and "out-of-range" in security.lower() and "non-finite" in security.lower() and "zero" in security.lower() and "visible" in security.lower() and "accessibility value" in security.lower(),
            "SECURITY must document battery/device-state privacy and the static baseline",
            failures)
    require("battery monitoring" in changes.lower() and "GitHub Actions" in changes and "make check" in changes and "make lint" in changes and "make test" in changes and "make build" in changes and "restores" in changes and
            "defer" in changes.lower() and "unknown" in changes.lower() and "out-of-range" in changes.lower() and "non-finite" in changes.lower() and "zero" in changes.lower() and "visible" in changes.lower() and "accessibility value" in changes.lower(),
            "CHANGES must record the battery monitoring fix, unknown-level normalization, deferred restoration, and baseline",
            failures)
    require("status: completed" in baseline_plan and "status: completed" in lifecycle_plan and
            "status: completed" in defer_plan and "status: completed" in unknown_level_plan,
            "plans must be marked completed",
            failures)
    require("status: completed" in make_gates_plan,
            "make gate aliases plan must be marked completed",
            failures)
    require("status: completed" in upper_bound_plan,
            "battery level upper-bound plan must be marked completed",
            failures)
    require("status: completed" in nonfinite_plan,
            "non-finite battery level plan must be marked completed",
            failures)
    require("status: completed" in zero_level_plan,
            "zero battery level plan must be marked completed",
            failures)
    require("status: completed" in display_plan,
            "visible battery-level plan must be marked completed",
            failures)
    require("status: completed" in accessibility_value_plan,
            "battery accessibility value plan must be marked completed",
            failures)
    require("status: completed" in ci_plan and "GitHub Actions" in ci_plan and "make check" in ci_plan,
            "CI baseline plan must record hosted make check verification",
            failures)
    require("status: completed" in hosted_validation_plan and "make check" in hosted_validation_plan,
            "hosted project validation plan must be completed and document make check",
            failures)
    require("status: completed" in swift_5_build_plan and "simulator" in swift_5_build_plan.lower(),
            "Swift 5 app build plan must be completed and document simulator verification",
            failures)
    require("permissions:\n  contents: read" in workflow,
            "Check workflow must use read-only repository permissions",
            failures)
    require("cancel-in-progress: true" in workflow and "runs-on: macos-15" in workflow and
            "timeout-minutes: 10" in workflow,
            "Check workflow must bound duplicate and long-running macOS jobs",
            failures)
    require("actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10" in workflow and
            "run: make check" in workflow,
            "Check workflow must pin checkout and run the canonical baseline",
            failures)

    if shutil.which("xcodebuild"):
        result = subprocess.run(
            [
                "xcodebuild",
                "-project", "ChargeMe.xcodeproj",
                "-target", "ChargeMe",
                "-configuration", "Debug",
                "-sdk", "iphonesimulator",
                "CODE_SIGNING_ALLOWED=NO",
                "build",
            ],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        require(result.returncode == 0,
                "xcodebuild could not compile ChargeMe for the simulator: " + result.stdout.strip(),
                failures)
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
