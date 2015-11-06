# -*- coding: utf-8 -*-
from unittest import TestCase
from gaius.cli import transform_to_message_format
from textwrap import dedent


class CliTests(TestCase):

    def test_should_transform_parameters_to_message(self):
        stack_name = 'sample-stack'
        parameters = 'parameter1=value1,parameter2=value2'

        expected_message = (
            '{'
            '"parameters": {'
            '"parameter1": "value1", '
            '"parameter2": "value2"'
            '}, '
            '"region": "eu-west-1", '
            '"stackName": "sample-stack", '
            '"version": 1'
            '}'
        )

        message = transform_to_message_format(stack_name, parameters)
        self.assertEquals(message, expected_message)
