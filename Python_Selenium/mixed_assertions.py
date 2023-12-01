from pytest_check import check
import pytest

"""
Mixed assertions use pytest_check soft assertions.
Mixed assertions add interrupt_test argument, once set to True if assertion fails rest of test is skipped. So assertion
behaves as a hard assertion. 
Contains only assertions actually used. If other assertion is needed it has to be added into this file.
"""

interrupt_message = "Rest of the test skipped as interrupt_test is set to True."


def equal(value_1, value_2, assertion_message="", interrupt_test=False):
	flag = check.equal(value_1, value_2, assertion_message)
	if not flag and interrupt_test:
		pytest.skip(interrupt_message)


def is_true(boolean_value, assertion_message="", interrupt_test=False):
	flag = check.is_true(boolean_value, assertion_message)
	if not flag and interrupt_test:
		pytest.skip(interrupt_message)


def is_in(value_1, value_2, assertion_message="", interrupt_test=False):
	flag = check.is_in(value_1, value_2, assertion_message)
	if not flag and interrupt_test:
		pytest.skip(interrupt_message)


def greater(value_1, value_2, assertion_message="", interrupt_test=False):
	flag = check.greater(value_1, value_2, assertion_message)
	if not flag and interrupt_test:
		pytest.skip(interrupt_message)
