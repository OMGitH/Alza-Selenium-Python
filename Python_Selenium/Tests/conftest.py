from selenium import webdriver
from test_data import TestData
import pytest
import os
from datetime import datetime


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


# Configuration of title of html report.
def pytest_html_report_title(report):
    report_title = "Test execution report, " + datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    report.title = report_title
    