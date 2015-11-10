# -*- coding: utf-8 -*-
from unittest import TestCase
from gaius import cli
from mock import patch
from mockito import when, verify, any as any_value, mock


class CliTests(TestCase):

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
            'mystack',
            'parameter1=value1,parameter2=value2',
            'my::topic::arn',
            'eu-west-1'
        )
