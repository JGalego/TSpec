#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Module TSPEC
A simple Python module that allows the user to create
Quality Center-compatible test specifications.
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'Galego, João (jgalego1990@gmail.com)'
__copyright__ = 'Copyright (c) 2017 João Galego'
__version__ = '0.0.1 (Hallucigenia)'

# Modules
import csv
from copy import copy
from string import maketrans
import logging

# Log Configuration
FORMAT = "%(levelname)-4s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.WARN)

# Constants
DEFAULT_TEST_SPEC_NAME = "<EMPTY>"
DEFAULT_TEST_ID = "<EMPTY>"
DEFAULT_STEP_ID = 0
DEFAULT_STEP_DESCRIPTION = "<EMPTY>"
DEFAULT_STEP_EXPECTED_RESULT = "N/A"

class TestStep(object):
    """TestStep Class"""
    def __init__(self, step_id=DEFAULT_STEP_ID, \
                description=DEFAULT_STEP_DESCRIPTION, \
                expected_result=DEFAULT_STEP_EXPECTED_RESULT, **kwargs):
        """TestStep constructor"""
        self.step_id = step_id
        self.description = description
        self.expected_result = expected_result
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        """TestStep String Representation"""
        return "\n\tStep ID: %s\n\tDescription: %s\n\tExpected Result: %s\n" \
                % (self.step_id, self.description, self.expected_result)

    def get_id(self):
        """Get Step ID"""
        return self.step_id

    def get_description(self):
        """Get Step Description"""
        return self.description

    def get_expected_result(self):
        """Get Step Expected Result"""
        return self.expected_result

    def set_id(self, step_id):
        """Set Step ID
        :param step_id unique step identifier"""
        self.step_id = step_id

    def set_description(self, description):
        """Set Step Description
        :param description step description"""
        self.description = description

    def set_expected_result(self, expected_result):
        """Set Step Expected Result
        :param expected_result step expected result"""
        self.expected_result = expected_result

    def reset(self):
        """Reset Step Info"""
        self.set_description(DEFAULT_STEP_DESCRIPTION)
        self.set_expected_result(DEFAULT_STEP_EXPECTED_RESULT)


class BasicTest(object):
    """BasicTest Class"""
    def __init__(self, test_id=DEFAULT_TEST_ID):
        """BasicTest Constructor
        :param test_id unique string identifier"""
        if isinstance(test_id, str):
            self.test_id = test_id
        else:
            logging.warn("Test ID must be a string")
            logging.debug("Casting '%s' as a string", str(test_id))
            self.test_id = str(test_id)
        self.basic_test_info = []
        self.steps = []

    def __str__(self):
        """BasicTest String Representation"""
        self.basic_test_info = list(self.steps)
        self.basic_test_info.insert(0, "\nTest ID: " + self.test_id)
        return "\t\n".join(map(str, self.basic_test_info))

    def get_id(self):
        """Get Test ID"""
        return self.test_id

    def set_id(self, test_id):
        """Set Test ID
        :param test_id unique string identifier"""
        if isinstance(test_id, str):
            self.test_id = test_id
        else:
            logging.error("Test ID must be a string")

    def validate_step_id(self, new_step_id):
        """Check if a candidate Step ID is valid
        :param new_step_id candidate step id"""
        is_valid = True
        for step in self.steps:
            if new_step_id == step.get_id():
                is_valid = False
                logging.error("Duplicated step ID '%s'", str(new_step_id))
                break
        return is_valid

    def get_test_step_by_id(self, step_id):
        """Get Test Step by ID
        :param step_id unique step identifier"""
        for step in self.steps:
            if step_id == step.get_id():
                return copy(step)

    def get_test_step_by_index(self, step_index):
        """Get Test Step by Index
        :param step_index step position in the list of steps"""
        return self.steps[step_index]

    def add_step(self, step_id=DEFAULT_STEP_ID, \
                       description=DEFAULT_STEP_DESCRIPTION, \
                       expected_result=DEFAULT_STEP_EXPECTED_RESULT):
        """Create and append a new test step
        :param step_id unique step identifier
        :param description step description
        :param expected_result step expected result"""
        if self.validate_step_id(step_id):
            self.steps.append(TestStep(step_id, description, expected_result))

    def append_test_step(self, step):
        """Append TestStep object
        :param step TestStep object"""
        if isinstance(step, TestStep):
            if self.validate_step_id(step.get_id()):
                self.steps.append(copy(step))
        else:
            logging.error("Expected %s object", TestStep)

    def append_test_steps(self, step_list):
        """Append a list of TestStep objects
        :param step_list list of TestStep objects"""
        if isinstance(step_list, list):
            validate_steps = [isinstance(step, TestStep) for step in step_list]
            all_valid_steps = all(validate_steps)
            if all_valid_steps:
                for step in step_list:
                    self.append_test_step(step)
            else:
                for is_valid in validate_steps:
                    if not is_valid:
                        invalid_step_idx = validate_steps.index(is_valid)
                        logging.error("ERROR: Test step #%d is invalid (Got: %s, Expected: %s)", \
                                invalid_step_idx, type(step_list[invalid_step_idx]), TestStep)
        else:
            logging.error("Got: %s, Expected: %s", type(step_list), list)


    def insert_test_step(self, step, step_index=-1):
        """Insert TestStep object
        :param step TestStep object
        :param step_index target step position"""
        if self.validate_step_id(step.get_id()):
            if step_index == -1:
                self.steps.insert(len(self.steps), copy(step))
            else:
                self.steps.insert(step_index, copy(step))

    def remove_test_step_by_id(self, step_id):
        """Remove Test Step by ID
        :param step_id unique step identifier"""
        del_idx = None
        for idx in range(len(self.steps)):
            if step_id == self.steps[idx].get_id():
                del_idx = idx
                break

        if del_idx:
            del self.steps[del_idx]
        else:
            logging.error("Found no test-step with ID '%s'", str(step_id))

    def remove_test_step_by_index(self, step_index):
        """Remove Test Step by Index
        :param step_index step position in the list of steps"""
        del self.steps[step_index]

    def move_test_step_by_id(self, step_id, new_step_index):
        """Move test step to a new indexed position (ID)
        :param step_id unique step identifier
        :param new_step_index new step position in the list of steps"""
        step = self.get_test_step_by_id(step_id)
        self.remove_test_step_by_id(step_id)
        self.insert_test_step(new_step_index, step)

    def move_test_step_by_index(self, old_step_index, new_step_index):
        """Move test step to a new indexed position (Index)
        :param old_step_index current step position in the list of steps
        :param new_step_index new step position in the list of steps"""
        step = self.get_test_step_by_index(old_step_index)
        self.remove_test_step_by_index(old_step_index)
        self.insert_test_step(new_step_index, step)

    def get_test_steps(self):
        """Get test steps"""
        return self.steps

    def translate_name(self, intab="!#*|$<>%.&/()=?+ ;:\\", outtab="____________________"):
        """Replace unwanted characters with maketrans
        :param intab list of unwanted/forbidden characters
        :param outab list of replacement characters"""
        transtab = maketrans(intab, outtab)
        self.test_id = self.test_id.translate(transtab)


class CustomTest(BasicTest):
    """CustomTest Class"""
    def __init__(self, **kwargs):
        """CustomTest Constructor"""
        BasicTest.__init__(self, "")
        for key, value in kwargs.items():
            setattr(self, key, value)


class QCTest(CustomTest):
    """QCTest Class"""
    def __init__(self, test_subject="", test_level="", test_area="", is_automated=False):
        """QCTest Constructor
        :param test_subject qc test plan path
        :param test_level test level
        :param test_area test area
        :param is_automated automation flag"""
        CustomTest.__init__(self, test_subject=test_subject, test_level=test_level, \
                                        test_area=test_area, is_automated=is_automated)


class TestSpec(object):
    """TestSpec Class"""
    def __init__(self, name=DEFAULT_TEST_SPEC_NAME, **kwargs):
        """TestSpec Constructor
        :param name test spec name"""
        self.name = name
        self.tests = []
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        """TestSpec String Representation"""
        print(self.name)
        return "".join(map(str, self.tests))

    def get_name(self):
        """Get Test Spec Name"""
        return self.name

    def set_name(self, name):
        """Set Test Spec Name"""
        self.name = name

    def validate_test_id(self, new_test_id):
        """Validate Test ID
        :param test_id unique string identifier"""
        if not isinstance(new_test_id, str):
            logging.error("Test ID must be a string")
            return False
        for test in self.tests:
            if new_test_id == test.get_id():
                logging.error("Test ID must be unique")
                return False
        return True

    def validate_test(self, test):
        """Validate Test
        :param test Test object"""
        if self.validate_test_id(test.get_id()):
            if len(self.tests) > 0:
                if test.__class__ != self.tests[0].__class__:
                    logging.error("All tests must belong to the same class")
                    return False
                else:
                    return True
            else:
                return True
        else:
            return False

    def add_test(self, test):
        """Add a Test object
        :param test Test object"""
        if self.validate_test(test):
            self.tests.append(copy(test))
        else:
            logging.error("Failed to add test")

    def remove_test_by_id(self, test_id):
        """Remove Test by Test ID
        :param test_id unique string identifier"""
        del_idx = None
        for idx in range(len(self.tests)):
            if test_id == self.tests[idx].get_id():
                del_idx = idx
                break
        if del_idx:
            del self.tests[del_idx]
        else:
            logging.error("Found no test with ID '%s'", test_id)

    def remove_test_by_index(self, test_idx):
        """Remove Test by Test Index
        :param test_idx test position in the list of tests"""
        del self.tests[test_idx]

    def convert_to_csv(self, csv_path="./tspec.csv", delimiter=','):
        """Convert TSpec object to CSV file
        :param csv_path new tspec csv path
        :param delimiter csv delimiter"""
        if len(self.tests) > 0:
            # Get test suplementary attributes
            test_attribs = self.tests[0].__dict__.keys()
            test_attribs = sorted([c for c in test_attribs if c not in BasicTest().__dict__.keys()])
            csv_columns = copy(test_attribs)
            # Add core columns
            csv_columns.insert(0, 'test_id')
            csv_columns.insert(1, 'step_id')
            csv_columns.insert(2, 'description')
            csv_columns.insert(3, 'expected_result')
            # http://www.pythonforbeginners.com/systems-programming/using-the-csv-module-in-python/
            try:
                ofile = open(csv_path, 'wt')
            except (OSError, IOError) as error:
                logging.error("Unable to open file '%s'", str(csv_path))
                raise error
            # csv writer
            try:
                writer = csv.writer(ofile, delimiter=delimiter)
            except (OSError, IOError) as error:
                ofile.close()
                logging.error("Unable to create csv.writer for file '%s'", str(csv_path))
                raise error
            # Write columns
            writer.writerow(csv_columns)
            for test in self.tests:
                for step in test.steps:
                    if test.steps.index(step) == 0:
                        csv_row = [test.get_id(), step.get_id(), \
                                                  step.get_description(), \
                                                  step.get_expected_result()]
                        for attrib in test_attribs:
                            csv_row.append(getattr(test, attrib))
                    else:
                        csv_row = [None, step.get_id(), \
                                         step.get_description(), \
                                         step.get_expected_result()]
                        for attrib in test_attribs:
                            csv_row.append(None)
                    # Write test-step
                    writer.writerow(csv_row)
            # Close csv file
            ofile.close()
        else:
            logging.error("Test Spec contains no tests")
