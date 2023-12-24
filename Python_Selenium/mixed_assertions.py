from pytest_check import check
import pytest
from report_log import logger

"""
Mixed assertions use pytest_check soft assertions.
Mixed assertions add interrupt_test argument, once set to True if assertion fails rest of test is skipped. So assertion
behaves as a hard assertion. 
Contains only assertions actually used. If other assertion is needed it has to be added into this file.
"""

assertion_pass_note = "Assertion PASSED: "
assertion_fail_note = "Assertion FAILED: "
interrupt_message = "Rest of the test skipped as interrupt_test is set to True."


def equal(value_1, value_2, assertion_pass_message, assertion_fail_message, interrupt_test=False):
	flag = check.equal(value_1, value_2, assertion_fail_message)
	if not flag and interrupt_test:
		assertion_fail_message = assertion_fail_note + assertion_fail_message + f" ({interrupt_message})"
		logger.warning(assertion_fail_message)
		pytest.skip(interrupt_message)
	elif not flag:
		assertion_fail_message = assertion_fail_note + assertion_fail_message
		logger.warning(assertion_fail_message)
	else:
		assertion_pass_message = assertion_pass_note + assertion_pass_message
		logger.debug(assertion_pass_message)


def is_true(boolean_value, assertion_pass_message, assertion_fail_message, interrupt_test=False):
	flag = check.is_true(boolean_value, assertion_fail_message)
	if not flag and interrupt_test:
		assertion_fail_message = assertion_fail_note + assertion_fail_message + f" ({interrupt_message})"
		logger.warning(assertion_fail_message)
		pytest.skip(interrupt_message)
	elif not flag:
		assertion_fail_message = assertion_fail_note + assertion_fail_message
		logger.warning(assertion_fail_message)
	else:
		assertion_pass_message = assertion_pass_note + assertion_pass_message
		logger.debug(assertion_pass_message)


def is_in(value_1, value_2, assertion_pass_message, assertion_fail_message, interrupt_test=False):
	flag = check.is_in(value_1, value_2, assertion_fail_message)
	if not flag and interrupt_test:
		assertion_fail_message = assertion_fail_note + assertion_fail_message + f" ({interrupt_message})"
		logger.warning(assertion_fail_message)
		pytest.skip(interrupt_message)
	elif not flag:
		assertion_fail_message = assertion_fail_note + assertion_fail_message
		logger.warning(assertion_fail_message)
	else:
		assertion_pass_message = assertion_pass_note + assertion_pass_message
		logger.debug(assertion_pass_message)


def greater(value_1, value_2, assertion_pass_message, assertion_fail_message, interrupt_test=False):
	flag = check.greater(value_1, value_2, assertion_fail_message)
	if not flag and interrupt_test:
		assertion_fail_message = assertion_fail_note + assertion_fail_message + f" ({interrupt_message})"
		logger.warning(assertion_fail_message)
		pytest.skip(interrupt_message)
	elif not flag:
		assertion_fail_message = assertion_fail_note + assertion_fail_message
		logger.warning(assertion_fail_message)
	else:
		assertion_pass_message = assertion_pass_note + assertion_pass_message
		logger.debug(assertion_pass_message)
