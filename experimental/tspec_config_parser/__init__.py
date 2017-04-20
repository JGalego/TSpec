#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Module TSPEC_CONFIG_PARSER
Experimental Test Spec configuration parser
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = 'Galego, João (jgalego1990@gmail.com)'
__copyright__ = 'Copyright (c) 2017 João Galego'
__version__ = '0.0.1 (Hallucigenia)'

import re
import logging
from copy import copy
from tspec import TestSpec
from tspec import CustomTest
from tspec import TestStep

# Log Configuration
FORMAT = "%(levelname)-4s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.WARN)

LEXER = {'BLANK_LINE': r"[\s\b\t\n]+|$^",
         'COMMENT': r"# (?P<comment>.*)",
         'TSPEC_NAME': r"TSPEC (?P<name>.*)",
         'ASSIGNMENT': r"(?P<var>.*)=(?P<value>.*)",
         'START_TEST': r"START_TEST (?P<test_id>.*)",
         'START_STEP': r"START_STEP (?P<step_id>.*)",
         'END_STEP': r"END_STEP.*",
         'DESCRIPTION': r"DESCRIPTION (?P<description>.*)",
         'RESULT': r"RESULT (?P<result>.*)",
         'END_TEST': r"END_TEST.*"}

def get_directive(line):
    """Parse line and get directive"""
    for directive, pattern in LEXER.iteritems():
        match = re.match(pattern, line)
        if match:
            return (directive, match.groupdict())
    return None

class TestSpecConfigParser(object):
    """TestSpecConfigParser Class"""
    def __init__(self, test_config):
        self.test_config = test_config
        self.choose_from = ""

    def check_directives(self):
        """Get a list of directives"""
        config = open(self.test_config)
        directive_list = []
        for line in config:
            directive_list.append(get_directive(line))
        return directive_list

    def validate_config(self):
        """Validate directives"""
        directive_list = [directive[0] for directive in self.check_directives()]
        return directive_list

    def generate_tspec(self):
        """Generate test spec from config file"""
        config = open(self.test_config)
        tspec = TestSpec()
        # Get TestSpec info
        temp_test = None
        temp_step = None
        for line in config:
            # debug
            is_directive = get_directive(line)
            if is_directive:
                directive_type = is_directive[0]
                directive_args = is_directive[1]
                if directive_type in ["BLANK_LINE", "COMMENT"]:
                    pass # ignore
                elif directive_type == "TSPEC_NAME":
                    tspec.set_name(directive_args['name'])
                elif directive_type == "ASSIGNMENT":
                    setattr(self, directive_args['var'], directive_args['value'])
                elif directive_type == "START_TEST":
                    temp_test = CustomTest()
                    temp_test.set_id(directive_args['test_id'])
                    temp_test.translate_name()
                elif directive_type == "END_TEST":
                    tspec.add_test(copy(temp_test))
                    temp_test = None
                elif directive_type == "START_STEP":
                    temp_step = TestStep(str(directive_args['step_id']))
                elif directive_type == "DESCRIPTION":
                    temp_step.set_description(directive_args['description'])
                elif directive_type == "RESULT":
                    temp_step.set_expected_result(directive_args['result'])
                elif directive_type == "END_STEP":
                    if isinstance(temp_test, CustomTest):
                        temp_test.append_test_step(copy(temp_step))
                    temp_step = None
        return tspec
