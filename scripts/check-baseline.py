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
HOSTED_XCTEST_PLAN = ROOT / "docs/plans/2026-06-12-hosted-xctest.md"
PRESENTATION_PLAN = ROOT / "docs/plans/2026-06-12-battery-presentation-normalization.md"
APPEARANCE_REFRESH_PLAN = ROOT / "docs/plans/2026-06-13-battery-view-appearance-refresh.md"
LOCATION_INDEPENDENT_MAKE_PLAN = ROOT / "docs/plans/2026-06-13-location-independent-make.md"
LIVE_REFRESH_PLAN = ROOT / "docs/plans/2026-06-14-live-battery-level-refresh.md"
DETERMINISTIC_LIFECYCLE_TEST_PLAN = ROOT / "docs/plans/2026-06-14-deterministic-battery-lifecycle-xctest.md"
STALE_NOTIFICATION_PLAN = ROOT / "docs/plans/2026-06-14-stale-battery-notification-guard.md"
EXPECTED_WORKFLOW = """name: Check

on:
  pull_request:
  push:
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: check-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  baseline:
    runs-on: macos-15
    timeout-minutes: 10
    steps:
      - name: Check out repository
        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3
        with:
          persist-credentials: false
      - name: Validate battery baseline and XCTest
        run: make test
"""
EXPECTED_MAKEFILE = """.PHONY: build check lint test

ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

lint: check

test: check
\t@if command -v xcodebuild >/dev/null 2>&1; then cd "$(ROOT)" && ./scripts/run-tests.sh; else printf '%s\\n' "Skipping XCTest: xcodebuild is not installed."; fi

build: check

check:
\t@python3 "$(ROOT)/scripts/check-baseline.py"
"""


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def markdown_section(text, heading):
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


def strip_swift_line_comments(text):
    stripped_lines = []
    for line in text.splitlines():
        output = []
        in_string = False
        escaped = False
        index = 0
        while index < len(line):
            character = line[index]
            if not in_string and character == "/" and index + 1 < len(line) and line[index + 1] == "/":
                break
            output.append(character)
            if character == '"' and not escaped:
                in_string = not in_string
            if character == "\\":
                escaped = not escaped
            else:
                escaped = False
            index += 1
        stripped_lines.append("".join(output))
    return "\n".join(stripped_lines)


def swift_function_body(text, signature):
    start = text.find(signature)
    if start == -1:
        return ""

    body_start = text.find("{", start)
    if body_start == -1:
        return ""

    depth = 0
    for index in range(body_start, len(text)):
        character = text[index]
        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth == 0:
                return text[body_start + 1:index]
    return ""


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
    swift_comment_fixture = 'let endpoint = "http://example.com/path" // trailing comment'
    require(strip_swift_line_comments(swift_comment_fixture) ==
            'let endpoint = "http://example.com/path" ',
            "Swift comment stripping must preserve quoted URL strings",
            failures)
    required_files = [
        ".gitignore",
        ".github/workflows/check.yml",
        "CHANGES.md",
        "Makefile",
        "README.md",
        "SECURITY.md",
        "VISION.md",
        "ChargeMe.xcodeproj/project.pbxproj",
        "ChargeMe.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
        "ChargeMe.xcodeproj/xcshareddata/xcschemes/ChargeMe.xcscheme",
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
        "docs/plans/2026-06-12-hosted-xctest.md",
        "docs/plans/2026-06-13-battery-view-appearance-refresh.md",
        "docs/plans/2026-06-13-location-independent-make.md",
        "docs/plans/2026-06-14-live-battery-level-refresh.md",
        "docs/plans/2026-06-14-deterministic-battery-lifecycle-xctest.md",
        "docs/plans/2026-06-14-stale-battery-notification-guard.md",
        "docs/readme-overview.svg",
        "scripts/run-tests.sh",
    ]

    for relative_path in required_files:
        require((ROOT / relative_path).is_file(), f"Required file missing: {relative_path}", failures)

    for xml_file in [
        "ChargeMe.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
        "ChargeMe.xcodeproj/xcshareddata/xcschemes/ChargeMe.xcscheme",
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
    active_view_controller = strip_swift_line_comments(view_controller)
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
    test_runner = read("scripts/run-tests.sh")
    shared_scheme = read("ChargeMe.xcodeproj/xcshareddata/xcschemes/ChargeMe.xcscheme")
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
    hosted_xctest_plan = HOSTED_XCTEST_PLAN.read_text(encoding="utf-8") if HOSTED_XCTEST_PLAN.exists() else ""
    presentation_plan = PRESENTATION_PLAN.read_text(encoding="utf-8") if PRESENTATION_PLAN.exists() else ""
    appearance_refresh_plan = APPEARANCE_REFRESH_PLAN.read_text(encoding="utf-8") if APPEARANCE_REFRESH_PLAN.exists() else ""
    location_independent_make_plan = LOCATION_INDEPENDENT_MAKE_PLAN.read_text(encoding="utf-8") if LOCATION_INDEPENDENT_MAKE_PLAN.exists() else ""
    live_refresh_plan = LIVE_REFRESH_PLAN.read_text(encoding="utf-8") if LIVE_REFRESH_PLAN.exists() else ""
    deterministic_lifecycle_test_plan = DETERMINISTIC_LIFECYCLE_TEST_PLAN.read_text(encoding="utf-8") if DETERMINISTIC_LIFECYCLE_TEST_PLAN.exists() else ""
    stale_notification_plan = STALE_NOTIFICATION_PLAN.read_text(encoding="utf-8") if STALE_NOTIFICATION_PLAN.exists() else ""
    workflow = read(".github/workflows/check.yml")
    view_did_load = swift_function_body(active_view_controller, "override func viewDidLoad")
    view_will_appear = swift_function_body(active_view_controller, "override func viewWillAppear")
    view_did_disappear = swift_function_body(active_view_controller, "override func viewDidDisappear")
    start_battery_updates = swift_function_body(active_view_controller, "func startBatteryLevelUpdates")
    stop_battery_updates = swift_function_body(active_view_controller, "func stopBatteryLevelUpdates")

    subprocess.check_call(["sh", "-n", "scripts/run-tests.sh"], cwd=ROOT)
    require((ROOT / "scripts/run-tests.sh").stat().st_mode & 0o111,
            "scripts/run-tests.sh must be executable",
            failures)

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
    require("setBatteryMonitoringEnabled(true)" in view_controller,
            "ViewController must enable battery monitoring before reading batteryLevel",
            failures)
    require("func readBatteryLevel() -> Float?" in view_controller and
            "configureBatteryLevelLabel()" in view_did_load and
            "displayBatteryLevel(readBatteryLevel())" not in view_did_load,
            "ViewController must configure without sampling during viewDidLoad",
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
    require(view_controller.count("let normalizedLevel = normalizedBatteryLevel(batteryLevel)") == 2 and
            view_controller.count("Double(normalizedLevel * 100.0)") == 2,
            "Battery presentation formatters must normalize values before displaying percentages",
            failures)
    require_order(
        view_will_appear,
        [
            "super.viewWillAppear(animated)",
            "startBatteryLevelUpdates()",
        ],
        "ViewController must start battery updates after super.viewWillAppear",
        failures,
    )
    require_order(
        start_battery_updates,
        [
            "if batteryLevelObserver == nil",
            "batteryUpdateGeneration += 1",
            "let updateGeneration = batteryUpdateGeneration",
            "wasBatteryMonitoringEnabled = batteryMonitoringEnabled()",
            "setBatteryMonitoringEnabled(true)",
            "batteryLevelObserver = NotificationCenter.default.addObserver",
            "UIDevice.batteryLevelDidChangeNotification",
            "queue: batteryNotificationQueue()",
            "[weak self]",
            "strongSelf.refreshBatteryLevel(for: updateGeneration)",
            "displayBatteryLevel(readBatteryLevel())",
        ],
        "ViewController must enable one battery observer before refreshing visible state",
        failures,
    )
    require_order(
        view_did_disappear,
        [
            "stopBatteryLevelUpdates()",
            "super.viewDidDisappear(animated)",
        ],
        "ViewController must stop battery updates when it disappears",
        failures,
    )
    require_order(
        stop_battery_updates,
        [
            "batteryUpdateGeneration += 1",
            "NotificationCenter.default.removeObserver(observer)",
            "batteryLevelObserver = nil",
            "setBatteryMonitoringEnabled(previousMonitoringState)",
            "wasBatteryMonitoringEnabled = nil",
        ],
        "ViewController must remove the exact observer and restore monitoring state",
        failures,
    )
    active_generation = swift_function_body(
        active_view_controller, "func isBatteryUpdateGenerationActive"
    )
    guarded_refresh = swift_function_body(
        active_view_controller, "func refreshBatteryLevel(for generation: Int)"
    )
    require("private var batteryUpdateGeneration = 0" in view_controller and
            "batteryLevelObserver != nil && generation == batteryUpdateGeneration" in active_generation and
            "guard isBatteryUpdateGenerationActive(generation) else" in guarded_refresh and
            "displayBatteryLevel(readBatteryLevel())" in guarded_refresh,
            "Battery callbacks must refresh only for the active observer generation",
            failures)
    require("private var batteryLevelObserver: NSObjectProtocol?" in view_controller and
            "private var wasBatteryMonitoringEnabled: Bool?" in view_controller and
            "deinit" in view_controller and "stopBatteryLevelUpdates()" in view_controller,
            "ViewController must retain and clean up battery update lifecycle identity",
            failures)
    require("func normalizedBatteryLevel(_ batteryLevel: Float) -> Float?" in view_controller and
            "!(batteryLevel >= 0.0 && batteryLevel <= 1.0)" in view_controller and "return nil" in view_controller,
            "ViewController must normalize unknown, non-finite, or out-of-range battery levels to nil",
            failures)
    require_order(
        view_controller,
        [
            "let wasBatteryMonitoringEnabled = batteryMonitoringEnabled()",
            "setBatteryMonitoringEnabled(true)",
            "defer {",
            "setBatteryMonitoringEnabled(wasBatteryMonitoringEnabled)",
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
            "testBatteryLevelTextShowsUnknownForInvalidValues" in tests and
            "Battery Level: Unknown" in tests and
            "testBatteryLevelAccessibilityValueShowsKnownPercentage" in tests and
            '"75%"' in tests and
            "testBatteryLevelAccessibilityValueShowsZeroPercentage" in tests and
            '"0%"' in tests and
            "testBatteryLevelAccessibilityValueShowsUnknownWhenMissing" in tests and
            "testBatteryLevelAccessibilityValueShowsUnknownForInvalidValues" in tests and
            "testViewAppearanceRefreshesVisibleAndAccessibleBatteryLevel" in tests and
            "controller.loadViewIfNeeded()" in tests and
            "XCTAssertEqual(controller.batteryReadCount, 0" in tests and
            "XCTAssertEqual(controller.batteryReadCount, 2)" in tests and
            'XCTAssertEqual(controller.batteryLevelLabel.text, "Battery Level: 25%")' in tests and
            'XCTAssertEqual(controller.batteryLevelLabel.accessibilityValue, "25%")' in tests and
            'XCTAssertEqual(controller.batteryLevelLabel.text, "Battery Level: 75%")' in tests and
            'XCTAssertEqual(controller.batteryLevelLabel.accessibilityValue, "75%")' in tests and
            "testBatteryNotificationRefreshesOnceWhileVisibleAndStopsAfterDisappearance" in tests and
            "UIDevice.batteryLevelDidChangeNotification" in tests and
            "Repeated appearances must retain one battery observer" in tests and
            "Hidden views must stop receiving battery notifications" in tests and
            "testBatteryMonitoringIsEnabledOnlyWhileVisible" in tests and
            "XCTAssertTrue(controller.stubbedBatteryMonitoringEnabled)" in tests and
            "XCTAssertFalse(controller.stubbedBatteryMonitoringEnabled)" in tests and
            "testStaleBatteryNotificationGenerationCannotRefreshLaterLifecycle" in tests and
            "XCTAssertTrue(controller.isBatteryUpdateGenerationActive(1))" in tests and
            "XCTAssertFalse(controller.isBatteryUpdateGenerationActive(1))" in tests and
            "XCTAssertTrue(controller.isBatteryUpdateGenerationActive(3))" in tests and
            "controller.refreshBatteryLevel(for: 1)" in tests and
            "A stale queued callback must not refresh a later lifecycle" in tests and
            "controller.refreshBatteryLevel(for: 3)" in tests and
            "override func batteryMonitoringEnabled() -> Bool" in tests and
            "return stubbedBatteryMonitoringEnabled" in tests and
            "override func setBatteryMonitoringEnabled(_ enabled: Bool)" in tests and
            "stubbedBatteryMonitoringEnabled = enabled" in tests and
            "override func batteryNotificationQueue() -> OperationQueue?" in tests and
            "return nil" in tests and
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
    require(makefile == EXPECTED_MAKEFILE,
            "Makefile must exactly preserve static and XCTest verification gates",
            failures)
    require("xcrun simctl list devices available" in test_runner and
            "IOS_DESTINATION" in test_runner and "IOS_SIMULATOR_NAME" in test_runner and
            '-scheme "$SCHEME"' in test_runner and '-destination "$DESTINATION"' in test_runner and
            "CODE_SIGNING_ALLOWED=NO" in test_runner and "test" in test_runner,
            "test runner must discover or accept a simulator and execute unsigned XCTest",
            failures)
    require("iPhone 5" not in test_runner,
            "test runner must not use a retired fixed simulator",
            failures)
    require(shared_scheme.count('BlueprintIdentifier = "7F2D99BC1B11626500668E52"') >= 2 and
            shared_scheme.count('BlueprintIdentifier = "7F2D99D11B11626500668E52"') >= 2 and
            '<TestableReference' in shared_scheme and 'skipped = "NO"' in shared_scheme,
            "shared scheme must build the app and execute ChargeMeTests",
            failures)
    require("make lint" in readme and "make test" in readme and "make build" in readme and "make check" in readme and "GitHub Actions" in readme and "ChargeMe.xcodeproj" in readme and "batteryMonitoringEnabled" in readme and
            "restore" in readme.lower() and "defer" in readme.lower() and "unknown" in readme.lower() and "out-of-range" in readme.lower() and "non-finite" in readme.lower() and "zero" in readme.lower(),
            "README must document static verification, project usage, and deferred battery monitoring restoration",
            failures)
    require("visible" in readme.lower() and "Battery Level: Unknown" in readme and "accessibility value" in readme.lower(),
            "README must document visible battery-level display behavior",
            failures)
    require("view appearance" in readme.lower(),
            "README must document battery refresh on view appearance",
            failures)
    require("absolute Makefile path" in readme and "any working directory" in readme,
            "README must document location-independent verification", failures)
    require("local-only" in readme.lower() and "battery" in readme.lower(),
            "README must document local-only battery data expectations",
            failures)
    require("scripts/check-baseline.py" in vision and "make lint" in vision and "make test" in vision and "make build" in vision and "GitHub Actions" in vision and "local-only" in vision.lower() and
            "defer" in vision.lower() and "unknown" in vision.lower() and "out-of-range" in vision.lower() and "non-finite" in vision.lower() and "zero" in vision.lower() and "visible" in vision.lower() and "accessibility value" in vision.lower(),
            "VISION must describe the current static privacy baseline",
            failures)
    require("view appearance" in vision.lower(),
            "VISION must preserve fresh battery reads on view appearance",
            failures)
    require("battery" in security.lower() and "make check" in security and "GitHub Actions" in security and "unknown" in security.lower() and "out-of-range" in security.lower() and "non-finite" in security.lower() and "zero" in security.lower() and "visible" in security.lower() and "accessibility value" in security.lower(),
            "SECURITY must document battery/device-state privacy and the static baseline",
            failures)
    require("view appearance" in security.lower(),
            "SECURITY must document appearance-scoped local battery refresh",
            failures)
    require("battery monitoring" in changes.lower() and "GitHub Actions" in changes and "make check" in changes and "make lint" in changes and "make test" in changes and "make build" in changes and "restores" in changes and
            "defer" in changes.lower() and "unknown" in changes.lower() and "out-of-range" in changes.lower() and "non-finite" in changes.lower() and "zero" in changes.lower() and "visible" in changes.lower() and "accessibility value" in changes.lower(),
            "CHANGES must record the battery monitoring fix, unknown-level normalization, deferred restoration, and baseline",
            failures)
    require("view appearance" in changes.lower(),
            "CHANGES must record appearance-time battery refresh",
            failures)
    require("Make verification target derive the checkout root" in changes and "external directories" in changes,
            "CHANGES must record location-independent verification", failures)
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
    require("status: completed" in hosted_xctest_plan and "make test" in hosted_xctest_plan and
            "hosted macOS XCTest run" in hosted_xctest_plan,
            "hosted XCTest plan must record the completed executable test contract",
            failures)
    require("status: completed" in appearance_refresh_plan and
            "All four Make gates" in appearance_refresh_plan and
            "hostile mutations" in appearance_refresh_plan.lower(),
            "battery view appearance plan must record completed status and actual verification",
            failures)
    live_refresh_verification = markdown_section(live_refresh_plan, "Verification Results")
    require("status: completed" in live_refresh_plan and
            "all six isolated hostile mutations were rejected" in live_refresh_verification.lower() and
            "xcodebuild was unavailable" in live_refresh_verification and
            "No battery or device state was logged" in live_refresh_verification,
            "live battery refresh plan must record completed local verification",
            failures)
    require("one observer and bounded" in read("CHANGES.md") and
            "retain one observer identity" in read("SECURITY.md") and
            "one observer that is removed on disappearance" in read("VISION.md") and
            "Keep battery notification observation idempotent" in read("AGENTS.md"),
            "live battery refresh guidance must remain synchronized",
            failures)
    require("func batteryMonitoringEnabled() -> Bool" in view_controller and
            "return UIDevice.current.isBatteryMonitoringEnabled" in view_controller and
            "func setBatteryMonitoringEnabled(_ enabled: Bool)" in view_controller and
            "UIDevice.current.isBatteryMonitoringEnabled = enabled" in view_controller and
            "func batteryNotificationQueue() -> OperationQueue?" in view_controller and
            "return OperationQueue.main" in view_controller,
            "Production battery lifecycle seams must preserve UIDevice and main-queue behavior",
            failures)
    deterministic_statuses = re.findall(r"(?mi)^status:\s*(.+?)\s*$", deterministic_lifecycle_test_plan)
    deterministic_verification = markdown_section(deterministic_lifecycle_test_plan, "Verification Completed")
    require(deterministic_statuses == ["completed"] and
            "Both old-head hosted macOS events failed" in deterministic_verification and
            "root and external-directory `make check`" in deterministic_verification and
            "six isolated hostile mutations" in deterministic_verification.lower() and
            "new exact head" in deterministic_verification,
            "deterministic lifecycle XCTest plan must record completed local and pending hosted evidence",
            failures)
    require("simulator tests isolated" in read("CHANGES.md") and
            "simulator tests isolated" in read("AGENTS.md"),
            "Project guidance must document deterministic battery lifecycle tests",
            failures)
    normalized_guidance = [
        " ".join(document.lower().split())
        for document in [readme, vision, security, changes, read("AGENTS.md")]
    ]
    require(all("stale queued battery callbacks" in document and
                "lifecycle generation" in document
                for document in normalized_guidance),
            "Project guidance must document stale battery callback rejection",
            failures)
    stale_notification_statuses = re.findall(
        r"(?mi)^status:\s*(.+?)\s*$", stale_notification_plan
    )
    stale_notification_verification = markdown_section(
        stale_notification_plan, "Verification Completed"
    )
    stale_notification_required = (
        "All four Make gates",
        "absolute Makefile check",
        "python3 -m py_compile scripts/check-baseline.py",
        "sh -n scripts/run-tests.sh",
        "Five isolated hostile mutations",
        "git diff --check",
        "xcodebuild was unavailable",
    )
    require(stale_notification_statuses == ["completed"]
            and all(item in stale_notification_verification
                    for item in stale_notification_required)
            and not re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b",
                              stale_notification_verification),
            "stale battery notification plan must record completed verification",
            failures)
    location_statuses = re.findall(r"(?mi)^status:\s*(.+?)\s*$", location_independent_make_plan)
    location_verification = markdown_section(location_independent_make_plan, "Verification Completed")
    location_required = ("Root and external-directory Make gates passed", "root-derivation mutation failed", "checker-invocation mutation failed", "XCTest-runner mutation failed", "plan-status mutation failed", "plan-evidence mutation failed", "documentation mutation failed")
    require(location_statuses == ["completed"] and all(item in location_verification for item in location_required) and not re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b", location_verification),
            "location-independent Make plan must record completed verification", failures)
    presentation_status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", presentation_plan)
    presentation_work = markdown_section(presentation_plan, "Work Completed")
    presentation_verification = markdown_section(
        presentation_plan, "Verification Completed"
    )
    require(presentation_status == ["completed"] and presentation_work,
            "battery presentation normalization plan must record one completed status and completed work",
            failures)
    require(presentation_verification and
            not re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b", presentation_verification),
            "battery presentation normalization plan must record finished verification without pending markers",
            failures)
    for evidence in [
        "make check",
        "make lint",
        "make test",
        "make build",
        "python3 -m py_compile scripts/check-baseline.py",
        "sh -n scripts/run-tests.sh",
        "git diff --check",
        "27394507895",
        "27394511486",
        "27394736468",
        "27402322921",
        "287335f16f78525ddbb899b0f7119bc7ab1555e3",
        "7dce00c264c429756336d5bc37d8d5f79513609f",
        "let normalizedLevel = normalizedBatteryLevel(batteryLevel)",
    ]:
        require(evidence in presentation_verification,
                f"battery presentation normalization plan must preserve verification evidence: {evidence}",
                failures)
    require(workflow == EXPECTED_WORKFLOW,
            "Check workflow must exactly match the bounded, credential-free macOS XCTest contract",
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
