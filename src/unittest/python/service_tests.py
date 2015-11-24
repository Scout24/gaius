
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from gaius.service import parse_parameters


class TestParseParameters(TestCase):

    def test_single_pair_should_be_parsed_correctly(self):
        self.assertEqual({'key1': 'value1'}, parse_parameters('key1=value1'))

    def test_double_pair_should_be_parsed_correctly(self):
        self.assertEqual({'key1': 'value1', 'key2': 'value2'},
                         parse_parameters('key1=value1,key2=value2'))
