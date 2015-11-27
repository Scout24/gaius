#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from gaius import cli


class CliTests(TestCase):

    @patch('gaius.service.receive')
    @patch('gaius.service.notify')
    @patch('gaius.cli.docopt')
    def test_should_communicate(self, mock_docopt, mock_notify, mock_receive):
        parameters = {
            '--stack': 'mystack',
            '--parameters': 'parameter1=value1,parameter2=value2',
            '--topic-arn': 'my::topic::arn',
            '--region': 'eu-west-1',
            '--back-channel': 'crassus-output'
        }
        mock_docopt.return_value = parameters
        cli.communicate()
        mock_notify.assert_called_once_with('mystack',
                                            'parameter1=value1,parameter2=value2',
                                            'my::topic::arn', 'eu-west-1')
        mock_receive.assert_called_once_with('crassus-output', 'mystack')
