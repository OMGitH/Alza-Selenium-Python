from selenium import webdriver
from test_data import TestData
import pytest
import os
from datetime import datetime
from utilities import (get_exception_error_name_possibly_screenshot, check_exception_error_occurred, log_exception_error, add_screenshots_to_html_report,
                       get_exception_error_log_record_from_previous_calls, html_report_log_section_manipulation, get_path_test_screenshots_folder,
                       add_urls_to_html_report_delete_urls_file, get_url_save_to_file, make_folders_if_dont_exist, get_webdrivers_selenium_version_save_to_pytest_metadata)
from Config.names_paths import reports_folder


# Fixture method for initialization of driver before each test runs, after each test version of webdrivers and Selenium are obtained for html
# report Environment table and driver is quit.
@pytest.fixture(params=["chrome", "firefox"])
def initialize_driver(request, metadata):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    if request.param == "firefox":
        driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(TestData.url)
    request.cls.driver = driver
    yield
    # Get version of webdrivers (Chrome, Firefox) and Selenium and save it to pytest metadata therefore add it to Environment section of html report.
    get_webdrivers_selenium_version_save_to_pytest_metadata(driver, metadata)
    driver.quit()


# Configuration of location and name of html report file.
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    make_folders_if_dont_exist(reports_folder)
    report_file = "Test_report_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".html"
    report_location = os.path.join(reports_folder, report_file)
    config.option.htmlpath = report_location


# Fixture method for getting report screenshots folder name from html report file name that is stored in pytest config and is
# created inside pytest_configure hook.
@pytest.fixture()
def get_report_screenshots_folder_name(pytestconfig):
    path_to_html_report = pytestconfig.getoption("htmlpath")
    report_screenshots_folder = path_to_html_report.split("\\")[-1].replace(".html", "")
    return report_screenshots_folder


# Take screenshot in case of exception or an error, create a log record about exception or error and add all screenshots
# to corresponding test in html report if test fails.
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])
    if report.when == "call":
        if report.failed:
            # Get path to folder where screenshots for actual test are stored.
            path_test_screenshots_folder = get_path_test_screenshots_folder(item)
            # Take screenshot and record url in case of an exception or an error, save it and create log record in html report.
            # There can be either exception or error not both.
            if check_exception_error_occurred(report.longreprtext):
                exception_error, screenshot_name = get_exception_error_name_possibly_screenshot(report.longreprtext, take_screenshot=True, item=item, path_test_screenshots_folder=path_test_screenshots_folder)
                url_report_link_title = get_url_save_to_file(item.cls.driver, screenshot_name)
                log_exception_error(screenshot_name, exception_error, url_report_link_title)
            # Add all screenshots from screenshots folder and urls from urls file to html report.
            add_screenshots_to_html_report(path_test_screenshots_folder, extras)
            add_urls_to_html_report_delete_urls_file(extras)
        report.extras = extras


# Configuration of html report title.
def pytest_html_report_title(report):
    report_title = "Test execution report, " + datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    report.title = report_title


# Configuration of tests log records in html report. Title "Captured stdout call" is changed to "Steps", under "Steps" there is added
# log record about exception or error (if occurred) from "Captured stdout teardown" section. Then date and time is removed at desired log
# records, section "Captured stdout teardown" is removed (if it doesn't contain any other info) as well as whole section "Captured log call"
# that is uncolored duplicate "Steps" section.
def pytest_html_results_table_html(report, data):
    exception_error_log_record = ""
    # If exception or error occurred, get actual exception or error and get log record about the exception or error that shall be added to "Steps".
    # The log record about exception or error is not present in "report" or "data" (at least not in time to use it and change html report).
    if check_exception_error_occurred(report.longreprtext):
        exception_error = get_exception_error_name_possibly_screenshot(report.longreprtext)
        exception_error_log_record = get_exception_error_log_record_from_previous_calls(exception_error)
    # Manipulations to rename section "Captured stdout call" to "Steps", to add log record about exception or error (if occurred)
    # to section "Steps", to remove date and time from log headers and log records about item removal and to remove whole sections
    # "Captured log call" and "Captured stdout teardown".
    html_report_log_section_manipulation(report, data, exception_error_log_record)
