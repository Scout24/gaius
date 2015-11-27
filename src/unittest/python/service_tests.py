#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from mock import patch, Mock

import boto3

from moto import mock_sqs

from gaius.service import (parse_parameters,
                           generate_message,
                           notify,
                           receive,
                           is_related_message)


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

    @patch('gaius.service.is_related_message')
    @mock_sqs
    def test_receive_should_read_message_and_process(self, mock_rel_massage):
        message_body = ('{ ' +
                        '"status": "UPDATE_IN_PROGRESS", ' +
                        '"timestamp": "2015-11-24T13:14:16.575Z", ' +
                        '"stack_name": "my-teststack", ' +
                        '"message": "User Initiated", ' +
                        '"emitter": "cloudformation"}')
        sqs = boto3.resource('sqs')
        queue = sqs.create_queue(QueueName='BACK_CHANNEL')
        queue.send_message(MessageBody=message_body)
        mock_rel_massage.return_value = False
        receive('BACK_CHANNEL', 'my-another-teststack', 'eu-west-1',
                poll_interval=1, num_attempts=1)
        mock_rel_massage.return_value = True
        receive('BACK_CHANNEL', 'my-teststack', 'eu-west-1',
                poll_interval=1, num_attempts=1)

    @patch('gaius.service.is_related_message')
    @mock_sqs
    def test_receive_should_react_on_final_massage(self, mock_rel_massage):
        message_body = ('{ ' +
                        '"status": "UPDATE_COMPLETE", ' +
                        '"timestamp": "2015-11-24T13:14:16.575Z", ' +
                        '"stack_name": "my-teststack", ' +
                        '"message": "User Initiated", ' +
                        '"emitter": "cloudformation", ' +
                        '"resourceType": "AWS::CloudFormation::Stack"}')
        sqs = boto3.resource('sqs')
        queue = sqs.create_queue(QueueName='BACK_CHANNEL')
        queue.send_message(MessageBody=message_body)
        mock_rel_massage.return_value = True
        receive('BACK_CHANNEL', 'my-teststack', 'eu-west-1',
                poll_interval=1, num_attempts=1)

    @patch('gaius.service.is_related_message')
    @mock_sqs
    def test_receive_should_log_error_massage(self, mock_rel_massage):
        message_body = ('{ ' +
                        '"status": "failure", ' +
                        '"timestamp": "2015-11-24T13:14:16.575Z", ' +
                        '"stack_name": "my-teststack", ' +
                        '"message": "User Initiated", ' +
                        '"emitter": "cloudformation", ' +
                        '"resourceType": "AWS::CloudFormation::Stack"}')
        sqs = boto3.resource('sqs')
        queue = sqs.create_queue(QueueName='BACK_CHANNEL')
        queue.send_message(MessageBody=message_body)
        mock_rel_massage.return_value = True
        receive('BACK_CHANNEL', 'my-teststack', 'eu-west-1',
                poll_interval=1, num_attempts=1)

    def test_check_if_message_related(self):
        self.assertTrue(is_related_message({'stackName': 'TestStack'},
                                           'TestStack'))
        self.assertFalse(is_related_message({'stackName': 'TestStack'},
                                            'AnotherTestStack'))
        self.assertTrue(is_related_message({}, 'AnotherTestStack'))
