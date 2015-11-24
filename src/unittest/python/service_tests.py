#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from mock import patch, Mock

import boto3

from moto import mock_sqs

from gaius.service import parse_parameters, generate_message, notify, receive


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


class TestNotify(TestCase):

    @patch('boto3.client')
    @patch('gaius.service.generate_message', Mock(return_value='MESSAGE'))
    def test_should_send_sns_message(self, boto3_mock):
        sns_client_mock = Mock()
        boto3_mock.return_value = sns_client_mock
        notify(None, None, 'ANY_ARN', None)
        sns_client_mock.publish.assert_called_once_with(TopicArn='ANY_ARN',
                                                        Message='"MESSAGE"')


class TestReceive(TestCase):

    @mock_sqs
    def test_receive_should_read_message(self):
        sqs = boto3.resource('sqs')
        queue = sqs.create_queue(QueueName='BACK_CHANNEL')
        queue.send_message(MessageBody='"MESSAGE"')
        receive('BACK_CHANNEL')

