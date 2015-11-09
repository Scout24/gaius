# -*- coding: utf-8 -*-
from unittest import TestCase
from gaius import cli
from mock import patch, Mock
from mockito import when, verify, unstub, any as any_value, mock, never


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

        message = cli.transform_to_message_format(stack_name, parameters)
        self.assertEquals(message, expected_message)

    @patch('gaius.crassus.notify_crassus')
    def test_send_message(self, notify_crassus_mock):
        cli.crassus = mock(cli.crassus)
        when(cli).docopt(any_value()).thenReturn({
            '--stack': 'mystack',
            '--parameters': 'parameter1=value1,parameter2=value2',
            '--topic-arn': 'my::topic::arn',
            '--region': 'eu-west-1'
        })

        cli.send_message()

        verify(cli.crassus).notify_crassus(
            'my::topic::arn',
            '{"parameters":'
                ' {"parameter1": "value1", "parameter2": "value2"},'
                ' "region": "eu-west-1", "stackName": "mystack",'
                ' "version": 1}',
                'eu-west-1'
        )
