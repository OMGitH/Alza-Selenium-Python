from selenium import webdriver
from test_data import TestData
import pytest
import os
from datetime import datetime
import pytest_html


@pytest.fixture(params=["chrome", "firefox"])
def initialize_driver(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    if request.param == "firefox":
        driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(TestData.url)
    request.cls.driver = driver
    yield
    driver.quit()


# Configuration of location and name of html report file.
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    report_folder = "Reports"
    report_file = "Test_report_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".html"
    report_location = report_folder + "/" + report_file
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)
    config.option.htmlpath = report_location


# Fixture method for getting report screenshots folder name from html report file name that is stored in pytest config and is
# created inside pytest_configure hook.
@pytest.fixture()
def get_report_screenshots_folder_name(pytestconfig):
    path_to_html_report = pytestconfig.getoption("htmlpath")
    report_screenshots_folder = path_to_html_report.split("/")[-1].replace(".html", "")
    return report_screenshots_folder


# Adding screenshots to corresponding test in html report if test fails.
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])
    if report.when == "call":
        if report.failed:
            # Getting folder names and path to screenshots folder. Report folder for screenshots has the same name as report file except for ".html".
            # Test folder for screenshots has the same name as test.
            report_screenshots_folder = item.config.option.htmlpath.split("/")[-1].replace(".html", "")
            test_screenshots_folder = item.name
            path_test_screenshots_folder = os.path.join(".\Reports\Screenshots", report_screenshots_folder, test_screenshots_folder)
            # If assertion failed and screenshot was taken and saved into desired folder, all screenshots from folder are added into html report.
            if os.path.exists(path_test_screenshots_folder):
                screenshots = os.scandir(path_test_screenshots_folder)
                for screenshot in screenshots:
                    # Reports folder has to be removed from path as apparently relative path here starts from html report file, so from Reports folder.
                    path_screenshot = screenshot.path.replace("\\Reports", "")
                    extras.append(pytest_html.extras.png(path_screenshot, screenshot.name))
        report.extras = extras


# Configuration of html report title.
def pytest_html_report_title(report):
    report_title = "Test execution report, " + datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    report.title = report_title


# Configuration of tests log records in html report. Title "Captured stdout call" is changed to "Steps". Whole section "Captured log call"
# is removed as it is uncolored duplicate of stdout logs.
def pytest_html_results_table_html(data):
    title_to_replace = "Captured stdout call"
    new_title = "Steps"
    section_to_remove = "Captured log call"
    index_item_to_remove = -1
    for i, s in enumerate(data):
        if title_to_replace in s:
            data[i] = s.replace(title_to_replace, new_title)
        if section_to_remove in s:
            index_item_to_remove = i
    if index_item_to_remove > -1:
        data.pop(index_item_to_remove)
