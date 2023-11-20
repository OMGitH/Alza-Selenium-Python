from selenium import webdriver
from Config.test_data import TestData
import pytest


@pytest.fixture
def initialize_driver(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(TestData.url)
    request.cls.driver = driver
    yield
    driver.quit()
