#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""TSpec Tests"""

import pytest
import tspec

__author__ = "João Galego"
__copyright__ = "João Galego (2017)"
__license__ = "none"

def test_teststep_default_values():
    """TestStep Constructor Default Values"""
    test_step = tspec.TestStep()
    assert test_step.get_id() == tspec.DEFAULT_STEP_ID
    assert test_step.get_description() == tspec.DEFAULT_STEP_DESCRIPTION
    assert test_step.get_expected_result() == tspec.DEFAULT_STEP_EXPECTED_RESULT

def test_basictest_default_values():
    """BasicTest Constructor Default Values"""
    basic_test = tspec.BasicTest()
    assert basic_test.get_id() == tspec.DEFAULT_TEST_ID

def test_testspec_default_values():
    """TestSpec Constructor Default Values"""
    test_spec = tspec.TestSpec()
    assert test_spec.get_name() == tspec.DEFAULT_TEST_SPEC_NAME

def test_teststep_set_id():
    """TestStep Set ID"""
    test_step = tspec.TestStep(0)
    assert test_step.get_id() == 0
    test_step.set_id(1)
    assert test_step.get_id() == 1

def test_teststep_set_description():
    """TestStep Set Description"""
    before_description = "Dummy Description"
    after_description = "Another Dummy Description"
    test_step = tspec.TestStep(description=before_description)
    assert test_step.get_description() == before_description
    test_step.set_description(after_description)
    assert test_step.get_description() == after_description

def test_teststep_set_expected_result():
    """TestStep Set Expected Result"""
    before_expected_result = "Dummy Expected Result"
    after_expected_result = "Another Dummy Expected Result"
    test_step = tspec.TestStep(expected_result=before_expected_result)
    assert test_step.get_expected_result() == before_expected_result
    test_step.set_expected_result(after_expected_result)
    assert test_step.get_expected_result() == after_expected_result

def test_teststep_reset():
    """TestStep Reset"""
    before_description = "Dummy Description"
    before_expected_result = "Dummy Expected Result"
    test_step = tspec.TestStep(description=before_description, \
                               expected_result=before_expected_result)
    assert test_step.get_description() == before_description
    assert test_step.get_expected_result() == before_expected_result
    test_step.reset()
    assert test_step.get_description() == tspec.DEFAULT_STEP_DESCRIPTION
    assert test_step.get_expected_result() == tspec.DEFAULT_STEP_EXPECTED_RESULT
