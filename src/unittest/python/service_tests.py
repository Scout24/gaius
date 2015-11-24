
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from gaius.service import parse_parameters, generate_message


class TestParseParameters(TestCase):

    def test_single_pair_should_be_parsed_correctly(self):
        self.assertEqual({'key1': 'value1'}, parse_parameters('key1=value1'))

    def test_double_pair_should_be_parsed_correctly(self):
        self.assertEqual({'key1': 'value1', 'key2': 'value2'},
                         parse_parameters('key1=value1,key2=value2'))


class TestGenerateMessage(TestCase):

    def test_should_assemble_message_correctly(self):
        expected = {
            'version': 1,
            'stackName': 'ANY_STACK',
            'region': 'ANY_REGION',
            'parameters': {'ANY_KEY': 'ANY_VALUE'}

        }
        received = generate_message('ANY_STACK',
                                    'ANY_KEY=ANY_VALUE',
                                    'ANY_REGION')
        self.assertEqual(expected, received)
