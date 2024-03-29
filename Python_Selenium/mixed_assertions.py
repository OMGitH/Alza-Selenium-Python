"""Mixed assertions use pytest_check soft assertions.
Mixed assertions add "interrupt_test" argument, once set to "True" if assertion fails rest of test is skipped. So assertion behaves as a hard assertion.
Note:
- Contains only assertions actually used. If other assertion is needed it has to be added into this file.
"""
from pytest_check import check
from utilities import process_assertion


def equal(value1, value2, assertion_pass_message, assertion_fail_message, driver, report_screenshots_folder, tmp_test_urls_file_path, interrupt_test=False):
	flag = check.equal(value1, value2, assertion_fail_message)
	process_assertion(driver, report_screenshots_folder, tmp_test_urls_file_path, "equal", flag, assertion_pass_message, assertion_fail_message, interrupt_test, value1=value1, value2=value2)


def is_true(boolean_value, assertion_pass_message, assertion_fail_message, driver, report_screenshots_folder, tmp_test_urls_file_path, interrupt_test=False):
	flag = check.is_true(boolean_value, assertion_fail_message)
	process_assertion(driver, report_screenshots_folder, tmp_test_urls_file_path, "is_true", flag, assertion_pass_message, assertion_fail_message, interrupt_test, boolean_value=boolean_value)


def is_in(value1, value2, assertion_pass_message, assertion_fail_message, driver, report_screenshots_folder, tmp_test_urls_file_path, interrupt_test=False):
	flag = check.is_in(value1, value2, assertion_fail_message)
	process_assertion(driver, report_screenshots_folder, tmp_test_urls_file_path, "is_in", flag, assertion_pass_message, assertion_fail_message, interrupt_test, value1=value1, value2=value2)


def greater(value1, value2, assertion_pass_message, assertion_fail_message, driver, report_screenshots_folder, tmp_test_urls_file_path, interrupt_test=False):
	flag = check.greater(value1, value2, assertion_fail_message)
	process_assertion(driver, report_screenshots_folder, tmp_test_urls_file_path, "greater", flag, assertion_pass_message, assertion_fail_message, interrupt_test, value1=value1, value2=value2)
