# -*- coding: utf-8 -*-
from unittest import TestCase
from gaius import cli
from mock import patch
from mockito import when, verify, any as any_value, mock


class CliTests(TestCase):

    def setUp(self):
        cli.crassus = mock(cli.crassus)
        cli.back_channel = mock(cli.back_channel)

    def test_send_message(self):
        when(cli).docopt(any_value()).thenReturn({
            '--stack': 'mystack',
            '--parameters': 'parameter1=value1,parameter2=value2',
            '--topic-arn': 'my::topic::arn',
            '--region': 'eu-west-1',
            '--back-channel': 'crassus-output'
        })

        cli.send_message()

        verify(cli.crassus).notify_crassus(
            'mystack',
            'parameter1=value1,parameter2=value2',
            'my::topic::arn',
            'eu-west-1'
        )
        verify(cli.back_channel).receive_messages('crassus-output')
