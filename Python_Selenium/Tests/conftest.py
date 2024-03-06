from os import path, remove
from datetime import datetime
from selenium import webdriver
import pytest
from Tests.test_data import url
from utilities import (get_exception_name_possibly_screenshot, check_exception_occurred, log_exception, add_screenshots_to_html_report,
                       get_exception_log_record_from_previous_calls, html_report_log_section_manipulation, get_path_test_screenshots_folder,
                       add_urls_to_html_report_delete_urls_file, get_url_save_to_file, make_folders_if_dont_exist, get_webdrivers_selenium_version_save_to_pytest_metadata,
                       change_date_format_subtitle_html_report)
from Config.config import browsers, path_urls_file, reports_folder


@pytest.fixture(params=browsers)
def setup_and_teardown(request, metadata):
    """Fixture function for setup (as precondition urls file is deleted if it exists (shall be deleted at the end of previous test after URLs
    are added to html report) and initialization of driver) before each test runs, and teardown after each test ran (version of webdrivers
    and Selenium are obtained for html report "Environment" table and driver is quit).
    """
    if path.exists(path_urls_file):
        remove(path_urls_file)
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "firefox":
        driver = webdriver.Firefox()
    else:
        raise ValueError(f"FAILED during setup phase: Browser value '{request.param}' is not supported. Supported values are 'chrome' and 'firefox', check browsers in config.py file. No screenshot taken, no URL recorded. Test execution stopped.")
    driver.maximize_window()
    driver.get(url)
    request.cls.driver = driver
    yield
    # Get version of webdrivers (Chrome, Firefox) and Selenium and save it to pytest metadata therefore add it to "Environment" section of html report.
    get_webdrivers_selenium_version_save_to_pytest_metadata(driver, metadata)
    driver.quit()


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Hook function used for configuration of location and name of html report file."""
    make_folders_if_dont_exist(reports_folder)
    report_file = "Test_report_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".html"
    report_location = path.join(reports_folder, report_file)
    config.option.htmlpath = report_location


@pytest.fixture(scope="session")
def get_report_screenshots_folder_name(pytestconfig):
    """Fixture function for getting report screenshots folder name from html report file name that is stored in pytest config and is created
    inside pytest_configure hook.
    """
    path_to_html_report = pytestconfig.getoption("htmlpath")
    report_screenshots_folder = path.splitext(path.basename(path_to_html_report))[0]
    return report_screenshots_folder


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """Hook function used for taking a screenshot in case of exception, creation of a log record about exception.
    Also for adding all screenshots and URLs to corresponding test in html report in case test fails.
    """
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])
    if report.when == "call":
        if report.failed:
            # Get path to folder where screenshots for actual test are stored.
            path_test_screenshots_folder = get_path_test_screenshots_folder(item)
            # Take screenshot and record URL in case of an exception, save it and create log record in html report.
            if check_exception_occurred(report.longreprtext):
                exception, screenshot_name = get_exception_name_possibly_screenshot(report.longreprtext, take_screenshot=True, item=item, path_test_screenshots_folder=path_test_screenshots_folder)
                url_report_link_title = get_url_save_to_file(item.cls.driver, screenshot_name)
                log_exception(screenshot_name, exception, url_report_link_title)
            # Add all screenshots from screenshots folder and URLs from urls file to html report.
            add_screenshots_to_html_report(path_test_screenshots_folder, extras)
            add_urls_to_html_report_delete_urls_file(extras)
        report.extras = extras


def pytest_html_report_title(report):
    """Hook function used for configuration of html report title."""
    report_title = "Test execution report, " + datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    report.title = report_title


def pytest_html_results_table_html(report, data):
    """Hook function used for configuration of tests log records in html report. Title "Captured stdout call" is changed to "Steps", under "Steps"
    there is added log record about exception (if occurred) from "Captured stdout teardown" section. Then date and time is removed
    at desired log records, section "Captured stdout teardown" is removed (if it doesn't contain any other info) as well as whole section
    "Captured log call" that is uncolored duplicate "Steps" section.
    """
    exception_log_record = ""
    # If exception occurred, get actual exception and get log record about the exception that shall be added to "Steps".
    # The log record about exception is not present in "report" or "data" (at least not in time to use it and change html report).
    if report.when == "call" and check_exception_occurred(report.longreprtext):
        exception = get_exception_name_possibly_screenshot(report.longreprtext)
        exception_log_record = get_exception_log_record_from_previous_calls(exception)
    # Manipulations to rename section "Captured stdout call" to "Steps", to add log record about exception (if occurred)
    # to section "Steps", to remove date and time from log headers and log records about item removal and to remove whole sections
    # "Captured log call" and "Captured stdout teardown".
    html_report_log_section_manipulation(report, data, exception_log_record)


def pytest_unconfigure(config):
    """Hook function called after whole test run is finished (even after pytest_sessionfinish hook), at that time actual html report file is created.
    Format of date in subtitle is changed directly in html report file.
    """
    path_actual_html_report_file = config.option.htmlpath
    change_date_format_subtitle_html_report(path_actual_html_report_file)
