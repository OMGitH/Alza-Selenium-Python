"""Mixed assertions use pytest_check soft assertions.
Mixed assertions add "interrupt_test" argument, once set to "True" if assertion fails rest of test is skipped. So assertion behaves as a hard assertion.
Note:
- Contains only assertions actually used. If other assertion is needed it has to be added into this file.
"""
from pytest_check import check
from utilities import process_assertion


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
