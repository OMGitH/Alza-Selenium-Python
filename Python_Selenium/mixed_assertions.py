from pytest_check import check
import pytest
from report_log import logger
import os
import inspect
from PIL import Image
from io import BytesIO

"""
Mixed assertions use pytest_check soft assertions.
Mixed assertions add "interrupt_test" argument, once set to "True" if assertion fails rest of test is skipped. So assertion behaves as a hard assertion. 
Contains only assertions actually used. If other assertion is needed it has to be added into this file.
"""

assertion_pass_note = "Assertion PASSED: "
assertion_fail_note = "Assertion FAILED: "
interrupt_message = "\n\t\t\t\t- Rest of the test skipped as 'interrupt_test' is set to 'True'."


def equal(driver, report_screenshots_folder, value1, value2, assertion_pass_message, assertion_fail_message, interrupt_test=False):
	flag = check.equal(value1, value2, assertion_fail_message)
	process_assertion(driver, report_screenshots_folder, "equal", flag, assertion_pass_message, assertion_fail_message, interrupt_test, value1=value1, value2=value2)


def is_true(driver, report_screenshots_folder, boolean_value, assertion_pass_message, assertion_fail_message, interrupt_test=False):
	flag = check.is_true(boolean_value, assertion_fail_message)
	process_assertion(driver, report_screenshots_folder, "is_true", flag, assertion_pass_message, assertion_fail_message, interrupt_test, boolean_value=boolean_value)


def is_in(driver, report_screenshots_folder, value1, value2, assertion_pass_message, assertion_fail_message, interrupt_test=False):
	flag = check.is_in(value1, value2, assertion_fail_message)
	process_assertion(driver, report_screenshots_folder, "is_in", flag, assertion_pass_message, assertion_fail_message, interrupt_test, value1=value1, value2=value2)


def greater(driver, report_screenshots_folder, value1, value2, assertion_pass_message, assertion_fail_message, interrupt_test=False):
	flag = check.greater(value1, value2, assertion_fail_message)
	process_assertion(driver, report_screenshots_folder, "greater", flag, assertion_pass_message, assertion_fail_message, interrupt_test, value1=value1, value2=value2)


# Method for processing test based on outcome of assertion like taking a screenshot if failed, stopping test execution or logging message.
def process_assertion(driver, report_screenshots_folder, assertion_type, flag, assertion_pass_message, assertion_fail_message, interrupt_test, value1="", value2="", boolean_value=""):
	if not flag and interrupt_test:
		screenshot_name = take_screenshot_assertion_failed(driver, report_screenshots_folder, assertion_type, value1, value2, boolean_value)
		assertion_fail_message = assertion_fail_note + assertion_fail_message + f"\n\t\t\t\t- Screenshot '{screenshot_name}' taken." + interrupt_message
		logger.warning(assertion_fail_message)
		pytest.skip(interrupt_message)
	elif not flag:
		screenshot_name = take_screenshot_assertion_failed(driver, report_screenshots_folder, assertion_type, value1, value2, boolean_value)
		assertion_fail_message = assertion_fail_note + assertion_fail_message + f"\n\t\t\t\t- Screenshot '{screenshot_name}' taken."
		logger.warning(assertion_fail_message)
	else:
		assertion_pass_message = assertion_pass_note + assertion_pass_message
		logger.debug(assertion_pass_message)


# Method for taking and saving screenshot if assertion fails. Name of the screenshot is similar to failed assertion so that it is clear which assertion
# it belongs to, thus contains assertion values, assertion type, name of test file and code line number inside test from which code leading to the assertion was executed.
# Screenshots for tests are saved under "Tests\Reports\Screenshots\<name of report>\<name of test>".
def take_screenshot_assertion_failed(driver, report_screenshots_folder, assertion_type, value1="", value2="", boolean_value=""):
	screenshot = take_screenshot_memory(driver)
	screenshot_name_path = create_screenshot_file_name_path_assertion_failed(report_screenshots_folder, assertion_type, value1, value2, boolean_value)
	save_screenshot_png_file(screenshot, screenshot_name_path["path"])
	return screenshot_name_path["name"]


# Method for getting test file name and code line number inside test from which code leading to the assertion was executed. This info is used in name of screenshot.
# Loops back through frames and looks for a frame that contains name of actual running test. From this frame name of file and code line number are obtained and returned.
# Because test file name is used in name of screenshot file "." is removed from it.
def get_test_filename_code_line_number(running_test_name):
	# Get only running test name without additional information like browser.
	running_test_name = running_test_name.split("[")[0].strip()
	previous_frame = inspect.currentframe().f_back
	while previous_frame.f_code.co_name != running_test_name:
		previous_frame = previous_frame.f_back
	test_filename = os.path.basename(previous_frame.f_code.co_filename)
	test_filename = test_filename.replace(".", "")
	code_line_number = previous_frame.f_lineno
	test_filename_code_line_number = f"{test_filename}{code_line_number}"
	return test_filename_code_line_number


# Method for getting name of the running test.
def get_running_test_name():
	running_test_name = os.environ.get("PYTEST_CURRENT_TEST").split(":")[-1].split(" ")[0]
	return running_test_name


# Method for taking screenshot into memory.
def take_screenshot_memory(driver):
	screenshot = driver.get_screenshot_as_png()
	return screenshot


# Method for creating name of screenshot file and path to it when assertion fails.
def create_screenshot_file_name_path_assertion_failed(report_screenshots_folder, assertion_type, value1="", value2="", boolean_value=""):
	running_test_name = get_running_test_name()
	test_filename_code_line_number = get_test_filename_code_line_number(running_test_name)
	test_screenshots_folder = running_test_name
	path_test_screenshots_folder = os.path.join(".\Reports\Screenshots", report_screenshots_folder, test_screenshots_folder)
	if not os.path.exists(path_test_screenshots_folder):
		os.makedirs(path_test_screenshots_folder)
	# Each screenshot name contains index based on number of already existing screenshots in corresponding folder.
	number_of_test_screenshots = len(os.listdir(path_test_screenshots_folder))
	screenshot_index = number_of_test_screenshots + 1
	# Screenshot name is created based on type of assertion.
	match assertion_type:
		case "equal":
			screenshot_name = f"Assert_failed{screenshot_index}-{value1}_equals_{value2}-({test_filename_code_line_number}).png"
		case "is_true":
			screenshot_name = f"Assert_failed{screenshot_index}-check_bool({boolean_value})-({test_filename_code_line_number}).png"
		case "is_in":
			screenshot_name = f"Assert_failed{screenshot_index}-{value1}_in_{value2}-({test_filename_code_line_number}).png"
		case "greater":
			screenshot_name = f"Assert_failed{screenshot_index}-{value1}_is_greater_than_{value2}-({test_filename_code_line_number}).png"
		case _:
			screenshot_name = "invalid.png"
	path_to_actual_screenshot = os.path.join(path_test_screenshots_folder, screenshot_name)
	screenshot_name_path = dict()
	screenshot_name_path["name"] = screenshot_name
	screenshot_name_path["path"] = path_to_actual_screenshot
	return screenshot_name_path


# Method for saving screenshot as png file.
def save_screenshot_png_file(screenshot, path_to_screenshot_file):
	# Transform screenshot into format that can be saved as png file.
	screenshot = Image.open(BytesIO(screenshot))
	screenshot.save(path_to_screenshot_file)
