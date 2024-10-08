"""Contains additional functions. Contains also functions directly related to assertions like process_assertion as if these functions were directly
inside mixed_assertions.py they would be offered via dot notation and that is not desired. There are also functions here used by functions in
conftest.py file which are defined here in order to keep conftest.py less complex.
"""
import os
from datetime import date
from inspect import currentframe
from io import BytesIO
from re import sub
import pytest
import pytest_html
from PIL import Image
from selenium import __version__
from Config.config import path_screenshots_folder, reports_folder
from report_logger import logger


# General functions:
def take_screenshot_into_memory(driver):
	"""Function for taking screenshot into memory."""
	screenshot = driver.get_screenshot_as_png()
	return screenshot


def save_screenshot_png_file(screenshot, path_to_screenshot_file):
	"""Function for saving screenshot from memory to png file."""
	# Transform screenshot into format that can be saved as png file.
	screenshot = Image.open(BytesIO(screenshot))
	screenshot.save(path_to_screenshot_file)


def make_folders_if_dont_exist(path_to_folders):
	"""Function for creation of folder or folder with sub folder(s)."""
	if not os.path.exists(path_to_folders):
		os.makedirs(path_to_folders)


def check_filename_is_correct(filename):
	"""Function for checking filename if it is correct, i.e. doesn't contain character that can't be present in filename."""
	restricted_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
	flag = True
	for char in restricted_chars:
		if char in filename:
			flag = False
			return flag
	return flag


def get_last_line_from_record(record):
	"""Function for getting last line from record.
	Note:
	- Can be used with failure record when looking for particular exception as it is mentioned at its last line. In such case
	as a "record" a "report.longreprtext" is used.
	"""
	record_last_line = ""
	if record != "":
		record_last_line = record.splitlines()[-1]
	return record_last_line


def get_calling_function_filename_code_line_number(calling_function):
	"""Function for getting filename and line number of code inside calling function.
	Note:
	- Can be used for getting test filename and code line number inside test from which code leading to the assertion was executed.
	This info is used in name of failed assertions screenshot.
	"""
	# Loop back through frames and look for a frame that contains name of calling function. From this frame name of file
	# and code line number are obtained.
	previous_frame = currentframe().f_back
	while previous_frame.f_code.co_name != calling_function:
		previous_frame = previous_frame.f_back
	calling_function_filename = os.path.basename(previous_frame.f_code.co_filename)
	code_line_number = previous_frame.f_lineno
	return calling_function_filename, code_line_number


# Functions related to assertions:
def process_assertion(driver, report_screenshots_folder, tmp_test_urls_file_path, assertion_type, flag, assertion_pass_message, assertion_fail_message, interrupt_test, value1="", value2="", boolean_value=""):
	"""Function for processing test execution based on outcome of assertion like taking a screenshot if failed, stopping test execution or logging a message."""
	assertion_pass_note = "Assertion PASSED: "
	assertion_fail_note = "Assertion FAILED: "
	interrupt_message = "\n\t\t\t\t- Rest of the test skipped as 'interrupt_test' is set to 'True'."

	if not flag and interrupt_test:
		screenshot_name = take_screenshot_assertion_failed(driver, report_screenshots_folder, assertion_type, value1, value2, boolean_value)
		url_report_link_title = get_url_save_to_file(driver, screenshot_name, tmp_test_urls_file_path)
		assertion_fail_message = assertion_fail_note + assertion_fail_message + f"\n\t\t\t\t- Screenshot '{screenshot_name}' taken." + f"\n\t\t\t\t- URL '{url_report_link_title}' recorded." + interrupt_message
		logger.warning(assertion_fail_message)
		pytest.skip(interrupt_message)
	elif not flag:
		screenshot_name = take_screenshot_assertion_failed(driver, report_screenshots_folder, assertion_type, value1, value2, boolean_value)
		url_report_link_title = get_url_save_to_file(driver, screenshot_name, tmp_test_urls_file_path)
		assertion_fail_message = assertion_fail_note + assertion_fail_message + f"\n\t\t\t\t- Screenshot '{screenshot_name}' taken." + f"\n\t\t\t\t- URL '{url_report_link_title}' recorded."
		logger.warning(assertion_fail_message)
	else:
		assertion_pass_message = assertion_pass_note + assertion_pass_message
		logger.debug(assertion_pass_message)


def take_screenshot_assertion_failed(driver, report_screenshots_folder, assertion_type, value1, value2, boolean_value):
	"""Function for taking and saving screenshot if assertion fails. Name of the screenshot is similar to failed assertion so that it is clear
	which assertion	it belongs to, thus contains assertion values, assertion type, name of test file and code line number inside test
	from which code leading to the assertion was executed. Screenshots for tests are saved under
	"Tests\Reports\Screenshots\<name of report>\<name of test>\<name of screenshot>.png".
	"""
	screenshot = take_screenshot_into_memory(driver)
	screenshot_name, path_to_actual_screenshot = create_screenshot_filename_path_assertion_failed(report_screenshots_folder, assertion_type, value1, value2, boolean_value)
	save_screenshot_png_file(screenshot, path_to_actual_screenshot)
	return screenshot_name


def create_screenshot_filename_path_assertion_failed(report_screenshots_folder, assertion_type, value1="", value2="", boolean_value=""):
	"""Function for creation of screenshot filename and path to it when assertion fails."""
	running_test_name_including_browser = os.environ.get("PYTEST_CURRENT_TEST").split(":")[-1].split(" ")[0]
	test_screenshots_folder = running_test_name_including_browser
	# Get only running test name without additional information like browser.
	running_test_name = running_test_name_including_browser.split("[")[0].strip()
	test_filename, code_line_number = get_calling_function_filename_code_line_number(running_test_name)
	# Because test filename is used in name of screenshot file "." is removed from it.
	test_filename_without_dot = test_filename.replace(".", "")
	test_filename_code_line_number = f"{test_filename_without_dot}{code_line_number}"
	path_test_screenshots_folder = os.path.join(path_screenshots_folder, report_screenshots_folder, test_screenshots_folder)
	make_folders_if_dont_exist(path_test_screenshots_folder)
	# Each failed assertion screenshot name contains index based on number of already existing screenshots in corresponding folder.
	number_of_test_screenshots = len(os.listdir(path_test_screenshots_folder))
	screenshot_index = number_of_test_screenshots + 1
	# Screenshot filename is created based on type of assertion. It may happen value1 or value2 contains character that is restricted in
	# filename, therefore screenshot_name is checked and if it is incorrect, values are removed from it.
	match assertion_type:
		case "equal":
			screenshot_name = f"Assert_failed{screenshot_index}-{value1}_equals_{value2}-({test_filename_code_line_number}).png"
			if not check_filename_is_correct(screenshot_name):
				screenshot_name = f"Assert_failed{screenshot_index}-equals-({test_filename_code_line_number}).png"
		case "is_true":
			screenshot_name = f"Assert_failed{screenshot_index}-check_bool({boolean_value})-({test_filename_code_line_number}).png"
		case "is_in":
			screenshot_name = f"Assert_failed{screenshot_index}-{value1}_in_{value2}-({test_filename_code_line_number}).png"
			if not check_filename_is_correct(screenshot_name):
				screenshot_name = f"Assert_failed{screenshot_index}-in-({test_filename_code_line_number}).png"
		case "greater":
			screenshot_name = f"Assert_failed{screenshot_index}-{value1}_is_greater_than_{value2}-({test_filename_code_line_number}).png"
			if not check_filename_is_correct(screenshot_name):
				screenshot_name = f"Assert_failed{screenshot_index}-is_greater_than-({test_filename_code_line_number}).png"
		case _:
			screenshot_name = f"Assert_failed{screenshot_index}-unknown_assertion_type-({test_filename_code_line_number}).png"
	path_to_actual_screenshot = os.path.join(path_test_screenshots_folder, screenshot_name)
	return screenshot_name, path_to_actual_screenshot


# Functions related to exceptions:
def check_exception_occurred(failure_record):
	"""Function for checking if exception occurred."""
	flag = False
	# Get last line of failure record, as name of exception is there.
	failure_record_last_line = get_last_line_from_record(failure_record)
	if failure_record_last_line != "":
		if "Exception" in failure_record_last_line or "Error" in failure_record_last_line:
			flag = True
	return flag


def get_exception_name(failure_record):
	"""Function for getting actual exception name if it occurred.
	Note:
	- Should be called only when there was an exception (i.e. when function "check_exception_occurred" returns "True").
	"""
	# Actual exception name is the last word at last line of failure record.
	failure_record_last_line = get_last_line_from_record(failure_record)
	exception_name = failure_record_last_line.split()[-1]
	exception_name = exception_name.strip()
	return exception_name


def get_exception_message(failure_record):
	"""Function for getting actual exception message (if it is present) if exception occurred.
	Note:
	- Should be called only when there was an exception (i.e. when function "check_exception_occurred" returns "True").
	"""
	exception_message = ""
	failure_record_lines = failure_record.splitlines()
	for line in failure_record_lines:
		if "Message:" in line:
			exception_message = line.split("Message:")[-1]
			exception_message = exception_message.strip()
			break
	return exception_message


def save_exception_screenshot_to_file(screenshot_in_memory, exception_name, path_test_screenshots_folder):
	"""Function for saving exception screenshot that is in memory to file with exception name (among failed assertions screenshots) once the exception occurred.
	Note:
	- Should be called only when there was an exception (i.e. when function "check_exception_occurred" returns "True").
	"""
	screenshot_name = f"{exception_name}.png"
	# If there is a character in exception name that cannot be present in filename then name of exception
	# is replaced by general "exception".
	if not check_filename_is_correct(screenshot_name):
		screenshot_name = "exception.png"
	path_screenshot_file = os.path.join(path_test_screenshots_folder, screenshot_name)
	make_folders_if_dont_exist(path_test_screenshots_folder)
	save_screenshot_png_file(screenshot_in_memory, path_screenshot_file)
	return screenshot_name


def log_exception(screenshot_name, exception_name, url_report_link_title, exception_msg):
	"""Function for creation of a log record in case of exception."""
	screenshot_message = f"\n\t\t\t\t- Screenshot '{screenshot_name}' taken."
	url_message = f"\n\t\t\t\t- URL '{url_report_link_title}' recorded."
	test_stop_message = f"\n\t\t\t\t- Test execution stopped."
	# If exception message is not empty, it is added to exception log record.
	if exception_msg:
		exception_message = f"\n\t\t\t\t- {exception_msg}"
		exception_log_message = f"'{exception_name}' occurred:" + exception_message + screenshot_message + url_message + test_stop_message
	else:
		exception_log_message = f"'{exception_name}' occurred:" + screenshot_message + url_message + test_stop_message
	logger.warning(exception_log_message)


def get_exception_log_record_from_previous_calls(exception):
	"""Function for obtaining log record about exception from previous calls by looping back through frames.
	Note:
	- Should be called only when there was an exception (i.e. when function "check_exception_occurred" returns "True").
	"""
	exception_log_record = ""
	separator = "\x1b[0m\n"
	# Loop back through frames and look for a frame that contains report from teardown phase and that contains in capstdout actual exception.
	# A list of log records is created from this frame capstdout and from this list the actual exception log record is obtained.
	# At the end there is a separator added to this record because as a separator formatting characters from end of log records are used.
	previous_frame = currentframe().f_back
	while not exception_log_record:
		if previous_frame.f_locals.get("report"):
			if previous_frame.f_locals["report"].when == "teardown" and exception in previous_frame.f_locals["report"].capstdout:
				log_records = previous_frame.f_locals["report"].capstdout.split(separator)
				for record in log_records:
					if exception in record:
						exception_log_record = record
						exception_log_record += separator
						break
		previous_frame = previous_frame.f_back
	return exception_log_record


# Functions related to assertions and exceptions:
def get_path_test_screenshots_folder(item):
	"""Function for getting path to folder where screenshots for particular test are stored."""
	# Report folder for screenshots has the same name as report file except for ".html".
	report_screenshots_folder = item.cls.report_screenshots_folder
	# Test folder for screenshots has the same name as test itself.
	test_screenshots_folder = item.name
	path_test_screenshots_folder = os.path.join(path_screenshots_folder, report_screenshots_folder, test_screenshots_folder)
	return path_test_screenshots_folder


def get_url_save_to_file(driver, screenshot_name, tmp_test_urls_file_path):
	"""Function for getting current URL address and saving it to a file. File is temporary just for actual test, it is handled by
	pytest fixture tmp_path.
	"""
	current_url_address = driver.current_url
	# Title of URL in report contains name of screenshot.
	url_report_link_title = screenshot_name.replace(".png", "")
	url_report_link_title = f"URL-{url_report_link_title}"
	# Each line in file represents one URL in format <title of URL in report>;<actual URL address>.
	urls_file_line = f"{url_report_link_title};{current_url_address}\n"
	# Open file or create and append current URL information.
	with open(tmp_test_urls_file_path, "a") as urls_file:
		urls_file.write(urls_file_line)
	return url_report_link_title


# Functions related to html report:
def html_report_log_section_manipulation(report, data, exception_log_record):
	"""Function for manipulation of log section of html report."""
	# Data manipulation to rename section "Captured stdout call" to "Steps", to add log record about exception (if occurred)
	# to section "Steps", to remove date and time from log headers and log records about item removal and to remove whole section "Captured log call".
	# Data manipulation has effect only when report is in "call" phase (there are 3 phases, first is "setup", second is "call" third is "teardown").
	if report.when == "call":
		title_to_replace = "Captured stdout call"
		new_title = "Steps"
		section_log_call_to_remove = "Captured log call"
		item_to_remove_index = -1
		section_captured_stdout_call_present = False
		for index, section in enumerate(data):
			# Renaming section "Captured stdout call" to "Steps", adding log record about exception to section "Steps", removing
			# date and time and setting presence of this section to "True".
			if title_to_replace in section:
				data[index] = section.replace(title_to_replace, new_title)
				data[index] += exception_log_record
				# Removing date and time:
				replace_by = r"                   \1"
				# From log headers.
				log_headers_pattern = "\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}(     -----)"
				data[index] = sub(log_headers_pattern, replace_by, data[index])
				# From log records when items are removed from basket, watchdogs or delivery addresses.
				items_removed_pattern = "\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}(     \t- \d )"
				data[index] = sub(items_removed_pattern, replace_by, data[index])
				# From log records when nothing is removed from basket, watchdogs or delivery addresses.
				nothing_removed_pattern = "\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}(     \t- Nothing removed as )"
				data[index] = sub(nothing_removed_pattern, replace_by, data[index])

				# Noting that "Captured stdout call" section was present.
				section_captured_stdout_call_present = True
			# Getting index of item in which section "Captured log call" is.
			if section_log_call_to_remove in section:
				item_to_remove_index = index
		# Removing item with section "Captured log call".
		if item_to_remove_index > -1:
			data.pop(item_to_remove_index)
		# In case there was no log record, section "Captured stdout call" is not created. If exception occurs then there will not be a
		# log record about this exception. In such a case it is needed to create this section with name "Steps" and with log record
		# about occurred exception and append it to "data" in order to make it present in html report.
		if not section_captured_stdout_call_present:
			section_header = "----------------------------- Steps -----------------------------\n"
			section_body = exception_log_record
			whole_section = section_header + section_body
			data.append(whole_section)
	# Removal of "Captured stdout teardown" section from html report has to be done on "report" object. If done on "data" it doesn't have any impact
	# on html report, the section stays there. It is removed only if "Captured stdout teardown" section doesn't contain any other information
	# than the exception log record, so if the section (that is a tuple) has 2 elements, header (section[0]) is "Captured stdout teardown"
	# and body (section[1]) contains "Screenshot '" (that is inside exception log record) and contains just one set of formatting characters
	# by which record begins (i.e. there is just one record) then the assumption is that it contains only record about that particular exception.
	# Teardown section is present only when report is in "teardown" phase (there are 3 phases, first is "setup", second is "call" third is "teardown").
	if report.when == "teardown":
		section_teardown_to_remove = "Captured stdout teardown"
		for index, section in enumerate(report.sections):
			if len(section) == 2 and section_teardown_to_remove == section[0] and "Screenshot '" in section[1] and section[1].count("\x1b[31m") == 1:
				report.sections.pop(index)
				break


def change_date_format_subtitle_html_report(path_actual_html_report_file):
	"""Function for changing date format in sentence below title in html report. It is done directly in report html file.
	At first whole content of current html report file is read by lines into list, then in list there is found line with sentence
	and in this sentence date is rewritten with today's date in correct format. Whole list with correction is then written into html report file.
	"""
	with open(path_actual_html_report_file, "r") as html_report:
		html_report_content_lines = html_report.readlines()

	todays_date = date.today()
	todays_date_formatted = todays_date.strftime("%d.%m.%Y")
	pattern = "(on) \d{2}-[a-zA-Z]*-\d{4} (at)"
	replace_by = rf"\1 {todays_date_formatted} \2"
	for index, line in enumerate(html_report_content_lines):
		if "<p>Report generated on" in line:
			html_report_content_lines[index] = sub(pattern, replace_by, line)
			break

	with open(path_actual_html_report_file, "w") as html_report:
		html_report.writelines(html_report_content_lines)


def add_screenshots_to_html_report(path_test_screenshots_folder, extras):
	"""Function for adding screenshots of failed assertions and exception to html report."""
	if os.path.exists(path_test_screenshots_folder):
		screenshots = os.scandir(path_test_screenshots_folder)
		path_separator = os.sep
		reports_folder_with_separator = reports_folder + path_separator
		for screenshot in screenshots:
			# "Reports" folder has to be removed from path as apparently relative path here starts from html report file, so from "Reports" folder.
			path_screenshot_file = screenshot.path.replace(reports_folder_with_separator, "")
			extras.append(pytest_html.extras.png(path_screenshot_file, screenshot.name))


def add_urls_to_html_report(extras, tmp_test_urls_file_path):
	"""Function for adding URLs of failed assertions and exception to html report."""
	if os.path.isfile(tmp_test_urls_file_path):
		with open(tmp_test_urls_file_path) as urls_file:
			for url in urls_file:
				url = url.strip()
				url = url.split(";")
				url_report_link_title = url[0]
				url_address = url[1]
				extras.append(pytest_html.extras.url(url_address, url_report_link_title))


def get_webdrivers_selenium_version_save_to_pytest_metadata(driver, metadata):
	"""Function for getting versions of webdriver(s) and Selenium and adding them to pytest metadata and thus adding them to "Environment" table
	of html report as html report takes content of "Environment" table from pytest metadata.
	"""
	# Get Selenium version and add it to pytest metadata if it is not there.
	if "Selenium" not in metadata.keys():
		selenium_version = __version__
		metadata["Selenium"] = selenium_version
	# Get version of webdrivers (Chrome, Firefox) and add them to pytest metadata if they are not there.
	if "Webdriver(s)" not in metadata.keys():
		metadata["Webdriver(s)"] = {}
	if "chrome" in driver.capabilities and "chrome" not in metadata["Webdriver(s)"].keys():
		driver_version = driver.capabilities['chrome']['chromedriverVersion'].split()[0]
		metadata["Webdriver(s)"]["chrome"] = driver_version
	if "moz:geckodriverVersion" in driver.capabilities and "firefox" not in metadata["Webdriver(s)"].keys():
		driver_version = driver.capabilities['moz:geckodriverVersion']
		metadata["Webdriver(s)"]["firefox"] = driver_version
