from PIL import Image
from io import BytesIO
import os
import inspect
import re
import pytest
from report_log import logger
import pytest_html

"""
Contains additional methods. Contains also methods directly related to assertions like process_assertion as if these methods were directly
inside mixed_assertions.py they would be offered via dot notation and that is not desired. There are also methods here used by methods in
conftest.py file which are defined here in order to keep conftest.py less complex.
"""


# Method for taking screenshot into memory.
def take_screenshot_memory(driver):
	screenshot = driver.get_screenshot_as_png()
	return screenshot


# Method for saving screenshot from memory to png file.
def save_screenshot_png_file(screenshot, path_to_screenshot_file):
	# Transform screenshot into format that can be saved as png file.
	screenshot = Image.open(BytesIO(screenshot))
	screenshot.save(path_to_screenshot_file)


# Method for creation of folder or folder with subfolder(s).
def make_folders_if_dont_exist(path_to_folders):
	if not os.path.exists(path_to_folders):
		os.makedirs(path_to_folders)


# Method for getting test file name and code line number inside test from which code leading to the assertion was executed.
# This info is used in name of failed assertions screenshot.
def get_test_filename_code_line_number(running_test_name):
	# Get only running test name without additional information like browser.
	running_test_name = running_test_name.split("[")[0].strip()
	# Loop back through frames and look for a frame that contains name of actual running test. From this frame name of file
	# and code line number are obtained.
	previous_frame = inspect.currentframe().f_back
	while previous_frame.f_code.co_name != running_test_name:
		previous_frame = previous_frame.f_back
	test_filename = os.path.basename(previous_frame.f_code.co_filename)
	code_line_number = previous_frame.f_lineno
	return test_filename, code_line_number


# Method for processing test execution based on outcome of assertion like taking a screenshot if failed, stopping test execution or logging a message.
def process_assertion(driver, report_screenshots_folder, assertion_type, flag, assertion_pass_message, assertion_fail_message, interrupt_test, value1="", value2="", boolean_value=""):
	assertion_pass_note = "Assertion PASSED: "
	assertion_fail_note = "Assertion FAILED: "
	interrupt_message = "\n\t\t\t\t- Rest of the test skipped as 'interrupt_test' is set to 'True'."

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
# Screenshots for tests are saved under "Tests\Reports\Screenshots\<name of report>\<name of test>\<name of screenshot>.png".
def take_screenshot_assertion_failed(driver, report_screenshots_folder, assertion_type, value1="", value2="", boolean_value=""):
	screenshot = take_screenshot_memory(driver)
	screenshot_name, path_to_actual_screenshot = create_screenshot_filename_path_assertion_failed(report_screenshots_folder, assertion_type, value1, value2, boolean_value)
	save_screenshot_png_file(screenshot, path_to_actual_screenshot)
	return screenshot_name


# Method for creating name of screenshot file and path to it when assertion fails.
def create_screenshot_filename_path_assertion_failed(report_screenshots_folder, assertion_type, value1="", value2="", boolean_value=""):
	running_test_name = os.environ.get("PYTEST_CURRENT_TEST").split(":")[-1].split(" ")[0]
	test_screenshots_folder = running_test_name
	test_filename, code_line_number = get_test_filename_code_line_number(running_test_name)
	# Because test filename is used in name of screenshot file "." is removed from it.
	test_filename_without_dot = test_filename.replace(".", "")
	test_filename_code_line_number = f'{test_filename_without_dot}{code_line_number}'
	path_test_screenshots_folder = os.path.join(".\Reports\Screenshots", report_screenshots_folder, test_screenshots_folder)
	make_folders_if_dont_exist(path_test_screenshots_folder)
	# Each failed assertion screenshot name contains index based on number of already existing screenshots in corresponding folder.
	number_of_test_screenshots = len(os.listdir(path_test_screenshots_folder))
	screenshot_index = number_of_test_screenshots + 1
	# Screenshot filename is created based on type of assertion.
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
	return screenshot_name, path_to_actual_screenshot


# Method for getting last line from record. Can be used with failure record when looking for particular exception or error as it is mentioned at its last line.
# As a "failure_record" is used "report.longreprtext" but it can be any record from which last line shall be obtained.
def get_last_line_from_record(failure_record):
	failure_message_last_line = ""
	if failure_record != "":
		failure_message_last_line = failure_record.splitlines()[-1]
	return failure_message_last_line


# Method for getting path to folder where screenshots for particular test are stored.
def get_path_test_screenshots_folder(item):
	# Get folder names and path to screenshots folder. Report folder for screenshots has the same name as report file except for ".html".
	# Test folder for screenshots has the same name as test itself.
	report_screenshots_folder = item.config.option.htmlpath.split("/")[-1].replace(".html", "")
	test_screenshots_folder = item.name
	path_test_screenshots_folder = os.path.join(".\Reports\Screenshots", report_screenshots_folder, test_screenshots_folder)
	return path_test_screenshots_folder


# Method for checking if exception or error occurred.
def check_exception_error_occurred(failure_record):
	flag = False
	# Get last line of failure record, as name of exception or error is there.
	failure_record_last_line = get_last_line_from_record(failure_record)
	if failure_record_last_line != "":
		if "Exception" in failure_record_last_line or "Error" in failure_record_last_line:
			flag = True
	return flag


# Method for getting actual exception or error if it occurred and also can be set to take screenshot (and save it to a file among failed assertions screenshots)
# of application once the exception or error occurred.
# Note:
# - Should be called only when there was an exception or error (i.e. when method "check_exception_error_occurred" returns True).
# - Method returns 1 or 2 values:
# - - In case screenshot shall NOT be taken, 1 value is returned (the exception or error itself as "exception_error").
# - - In case screenshot shall be taken, 2 values are returned ("exception_error" and "screenshot_name").
def get_exception_error_name_possibly_screenshot(failure_record, take_screenshot=False, item="", path_test_screenshots_folder=""):
	# Get last line of failure record, as name of exception or error is there.
	failure_record_last_line = get_last_line_from_record(failure_record)
	if take_screenshot:
		# If set to "True" takes screenshot into memory as soon as possible.
		driver = item.cls.driver
		screenshot = take_screenshot_memory(driver)
	fail_words = ["Exception", "Error"]
	for fail_word in fail_words:
		# Get all words containing "Exception" or "Error" that are at last line of failure record.
		exceptions_errors = re.findall(f"[a-zA-Z]*{fail_word}[a-zA-Z]*", failure_record_last_line)
		if exceptions_errors:
			# Get actual exception or error by returning the last occurrence of the word as the actual exception or error
			# is mentioned at the end of failure record.
			exception_error = exceptions_errors[-1]
			if take_screenshot:
				screenshot_name = f"{exception_error}.png"
				path_screenshot_file = os.path.join(path_test_screenshots_folder, screenshot_name)
				make_folders_if_dont_exist(path_test_screenshots_folder)
				save_screenshot_png_file(screenshot, path_screenshot_file)
				return exception_error, screenshot_name
			return exception_error


# Method for creation of a log record in case of exception or error.
def log_exception_error(screenshot_name, exception_error):
	screenshot_message = f"\n\t\t\t\t- Screenshot '{screenshot_name}' taken."
	test_stop_message = f"\n\t\t\t\t- Test execution stopped."
	exception_error_message = f"'{exception_error}' occurred." + screenshot_message + test_stop_message
	logger.warning(exception_error_message)


# Method for adding screenshots of failed assertions and exception or error to html report.
def add_screenshots_to_html_report(path_test_screenshots_folder, extras):
	if os.path.exists(path_test_screenshots_folder):
		screenshots = os.scandir(path_test_screenshots_folder)
		for screenshot in screenshots:
			# "Reports" folder has to be removed from path as apparently relative path here starts from html report file, so from "Reports" folder.
			path_screenshot_file = screenshot.path.replace("\\Reports", "")
			extras.append(pytest_html.extras.png(path_screenshot_file, screenshot.name))


# Method for obtaining log record about exception or error from previous calls by looping back through frames.
# Note:
# - Should be called only when there was an exception or error (i.e. when method "check_exception_error_occurred" returns True).
def get_exception_error_log_record_from_previous_calls(exception_error):
	exception_error_log_record = ""
	separator = "\x1b[0m\n"
	# Loop back through frames and look for a frame that contains report from teardown phase and that contains in capstdout actual exception
	# or error. A list of log records is created from this frame capstdout and from this list the actual exception or error log record is obtained.
	# At the end there is a separator added to this record because as a separator formatting characters from end of log records are used.
	previous_frame = inspect.currentframe().f_back
	while not exception_error_log_record:
		if previous_frame.f_locals.get("report"):
			if previous_frame.f_locals["report"].when == "teardown" and exception_error in previous_frame.f_locals["report"].capstdout:
				log_records = previous_frame.f_locals["report"].capstdout.split(separator)
				for record in log_records:
					if exception_error in record:
						exception_error_log_record = record
						exception_error_log_record += separator
						break
		previous_frame = previous_frame.f_back
	return exception_error_log_record


# Method for manipulation of log section of html report.
def html_report_log_section_manipulation(report, data, exception_error_log_record):
	# Data manipulation to rename section "Captured stdout call" to "Steps", to add log record about exception or error (if occurred)
	# to section "Steps" and to remove whole section "Captured log call".
	# Data manipulation has effect when report is in "call" phase (there are 3 phases, first is "setup", second is "call" third is "teardown").
	if report.when == "call":
		title_to_replace = "Captured stdout call"
		new_title = "Steps"
		section_log_call_to_remove = "Captured log call"
		item_to_remove_index = -1
		section_captured_stdout_call_present = False
		for i, s in enumerate(data):
			# Renaming section "Captured stdout call" to "Steps", adding log record about exception or error to section "Steps" and setting
			# presence of this section to "True".
			if title_to_replace in s:
				data[i] = s.replace(title_to_replace, new_title)
				data[i] += exception_error_log_record
				section_captured_stdout_call_present = True
			# Getting index of item in which section "Captured log call" is.
			if section_log_call_to_remove in s:
				item_to_remove_index = i
		# Removing item with section "Captured log call".
		if item_to_remove_index > -1:
			data.pop(item_to_remove_index)
		# In case there was no log record, section "Captured stdout call" is not created. If exception or error occurs then there will not be a
		# log record about this exception on error. In such a case it is needed to create this section with name "Steps" and with log record
		# about occurred exception or error and append it to "data" in order to make it present in html report.
		if not section_captured_stdout_call_present:
			section_header = "----------------------------- Steps -----------------------------\n"
			section_body = exception_error_log_record
			whole_section = section_header + section_body
			data.append(whole_section)
	# Removal of "Captured stdout teardown" section from html report has to be done on "report" object. If done on "data" it doesn't have any impact
	# on html report, the section stays there. It is removed only if "Captured stdout teardown" section doesn't contain any other information
	# than the exception or error log record, so if the section (that is a tuple) has 2 elements, header (section[0]) is "Captured stdout teardown"
	# and body (section[1]) contains "Screenshot '" (that is inside exception or error log record) and contains just one set of formatting characters
	# by which record begins (i.e. there is just one record) then the assumption is that it contains only record about that particular exception or error.
	# Teardown section is present only when report is in "teardown" phase (there are 3 phases, first is "setup", second is "call" third is "teardown").
	if report.when == "teardown":
		section_teardown_to_remove = "Captured stdout teardown"
		for index, section in enumerate(report.sections):
			if len(section) == 2 and section_teardown_to_remove == section[0] and "Screenshot '" in section[1] and section[1].count("\x1b[31m") == 1:
				report.sections.pop(index)
				break
