#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest2 import TestCase

from mock import patch, Mock

import boto3

from moto import mock_sqs

from gaius.service import (
    parse_parameters, generate_message, notify, receive, cleanup,
    cleanup_old_messages, is_related_message, DeploymentErrorException,
    credentials_set, credentials_reset, _credentials)


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

    @patch('boto3.resource')
    @patch('gaius.service.generate_message', Mock(return_value='MESSAGE'))
    def test_should_send_sns_message(self, boto3_mock):
        sns_resource_mock = Mock()
        sns_topic_mock = Mock()
        boto3_mock.return_value = sns_resource_mock
        sns_resource_mock.Topic.return_value = sns_topic_mock

        notify(None, None, 'ANY_ARN', None)
        sns_topic_mock.publish.assert_called_once_with(Message='"MESSAGE"')


class TestCredentials(TestCase):

    """
    The service module should be able to use different credentials than
    specified via the environment.

    This way, gaius can be used as a generic API for communicating with
    crassus, not just as a commandline tool.
    """

    def test_credentials_set_reset(self):
        """Check empty, set, test, reset, test."""
        empty_setting = {
            'AccessKeyId': None,
            'SecretAccessKey': None,
            'SessionToken': None
        }
        nonempty_setting = {
            'AccessKeyId': '1',
            'SecretAccessKey': '2',
            'SessionToken': '3'
        }
        self.assertEqual(_credentials, empty_setting)
        credentials_set(nonempty_setting)
        self.assertEqual(_credentials, nonempty_setting)
        credentials_reset()
        self.assertEqual(_credentials, empty_setting)


class TestCleanup(TestCase):

    @mock_sqs
    def test_cleanup_should_remove_old_message(self):
        message_body = (
            '{ '
            '"status": "UPDATE_COMPLETE", '
            '"timestamp": "2015-11-24T13:14:16.575Z", '
            '"stackName": "my-teststack", '
            '"message": "User Initiated", '
            '"emitter": "cloudformation", '
            '"resourceType": "AWS::CloudFormation::Stack"}')
        sqs = boto3.resource('sqs')
        queue = sqs.create_queue(QueueName='BACK_CHANNEL')
        queue.send_message(MessageBody=message_body)
        queue.send_message(MessageBody=message_body)
        cleanup('BACK_CHANNEL', 600, 'my-teststack', 'eu-west-1')

    @mock_sqs
    @patch('gaius.service.cleanup_old_messages')
    def test_cleanup_should_stop_on_timout_eq_0(
            self, mock_cleanup_old_messages):
        message_body = (
            '{ '
            '"status": "UPDATE_COMPLETE", '
            '"timestamp": "2015-11-24T13:14:16.575Z", '
            '"stackName": "my-teststack", '
            '"message": "User Initiated", '
            '"emitter": "cloudformation", '
            '"resourceType": "AWS::CloudFormation::Stack"}')
        sqs = boto3.resource('sqs')
        queue = sqs.create_queue(QueueName='BACK_CHANNEL')
        queue.send_message(MessageBody=message_body)
        cleanup('BACK_CHANNEL', 0, 'my-teststack', 'eu-west-1')
        self.assertFalse(mock_cleanup_old_messages.called)

    @mock_sqs
    def test_cleanup_should_not_delete_other_stacks_messages(self):
        message_body = (
            '{ '
            '"status": "UPDATE_COMPLETE", '
            '"timestamp": "2015-11-24T13:14:16.575Z", '
            '"stackName": "other-teststack", '
            '"message": "User Initiated", '
            '"emitter": "cloudformation", '
            '"resourceType": "AWS::CloudFormation::Stack"}')
        message = Mock()
        message.body = message_body
        self.assertIsNone(cleanup_old_messages(message, 'my-teststack'))


class TestReceive(TestCase):

    @patch('gaius.service.is_related_message')
    @mock_sqs
    def test_receive_should_read_message_and_process(self, mock_rel_message):
        message_body = (
            '{ '
            '"status": "UPDATE_IN_PROGRESS", '
            '"timestamp": "2015-11-24T13:14:16.575Z", '
            '"stackName": "my-teststack", '
            '"message": "User Initiated", '
            '"emitter": "cloudformation"}')
        sqs = boto3.resource('sqs')
        queue = sqs.create_queue(QueueName='BACK_CHANNEL')
        queue.send_message(MessageBody=message_body)

        mock_rel_message.return_value = False
        with self.assertRaisesRegexp(
                DeploymentErrorException,
                'No final CFN message was received after 1 seconds'):
            receive('BACK_CHANNEL', 1, 'my-another-teststack', 'eu-west-1',
                    poll_interval=1)

        with self.assertRaisesRegexp(
                DeploymentErrorException,
                'No final CFN message was received after 1 seconds'):
            receive('BACK_CHANNEL', 1, 'my-teststack', 'eu-west-1',
                    poll_interval=1)

    @patch('gaius.service.is_related_message')
    @mock_sqs
    def test_receive_should_react_on_final_massage(self, mock_rel_massage):
        message_body = (
            '{ '
            '"status": "UPDATE_COMPLETE", '
            '"timestamp": "2015-11-24T13:14:16.575Z", '
            '"stackName": "my-teststack", '
            '"message": "User Initiated", '
            '"emitter": "cloudformation", '
            '"resourceType": "AWS::CloudFormation::Stack"}')
        sqs = boto3.resource('sqs')
        queue = sqs.create_queue(QueueName='BACK_CHANNEL')
        queue.send_message(MessageBody=message_body)
        mock_rel_massage.return_value = True
        receive('BACK_CHANNEL', 600, 'my-teststack', 'eu-west-1',
                poll_interval=1)

    @patch('gaius.service.is_related_message')
    @mock_sqs
    def test_receive_should_fail_on_cfn_error_massage(self, mock_rel_massage):
        message_body = (
            '{ '
            '"status": "CREATE_FAILED", '
            '"timestamp": "2015-11-24T13:14:16.575Z", '
            '"stackName": "my-teststack", '
            '"message": "User Initiated", '
            '"emitter": "cloudformation", '
            '"resourceType": "AWS::CloudFormation::Stack"}')
        sqs = boto3.resource('sqs')
        queue = sqs.create_queue(QueueName='BACK_CHANNEL')
        queue.send_message(MessageBody=message_body)
        mock_rel_massage.return_value = True
        with self.assertRaisesRegexp(
                DeploymentErrorException,
                'Crassus failed with "User Initiated"'):
            receive('BACK_CHANNEL', 600, 'my-teststack', 'eu-west-1',
                    poll_interval=1)

    @patch('gaius.service.is_related_message')
    @mock_sqs
    def test_receive_should_fail_on_no_cnf_message(self, mock_rel_massage):
        message_body = (
            '{ '
            '"status": "CREATE_FAILED", '
            '"timestamp": "2015-11-24T13:14:16.575Z", '
            '"stackName": "my-teststack", '
            '"message": "User Initiated", '
            '"emitter": "cloudformation", '
            '"resourceType": "foo"}')
        sqs = boto3.resource('sqs')
        queue = sqs.create_queue(QueueName='BACK_CHANNEL')
        queue.send_message(MessageBody=message_body)
        mock_rel_massage.return_value = True
        with self.assertRaisesRegexp(
                DeploymentErrorException,
                'No final CFN message was received after 1 seconds'):
            receive('BACK_CHANNEL', 1, 'my-teststack', 'eu-west-1',
                    poll_interval=1)

    @patch('gaius.service.is_related_message')
    @mock_sqs
    def test_receive_should_log_error_massage(self, mock_rel_massage):
        message_body = (
            '{ '
            '"status": "failure", '
            '"timestamp": "2015-11-24T13:14:16.575Z", '
            '"stackName": "my-teststack", '
            '"message": "User Initiated", '
            '"emitter": "cloudformation", '
            '"resourceType": "AWS::CloudFormation::Stack"}')
        sqs = boto3.resource('sqs')
        queue = sqs.create_queue(QueueName='BACK_CHANNEL')
        queue.send_message(MessageBody=message_body)
        mock_rel_massage.return_value = True
        with self.assertRaisesRegexp(
                DeploymentErrorException,
                'Crassus failed with "User Initiated"'):
            receive('BACK_CHANNEL', 600, 'my-teststack', 'eu-west-1',
                    poll_interval=1)

    def test_check_if_message_related(self):
        self.assertTrue(
            is_related_message({'stackName': 'TestStack'}, 'TestStack'))
        self.assertFalse(is_related_message(
            {'stackName': 'TestStack'}, 'AnotherTestStack'))
        self.assertTrue(is_related_message({}, 'AnotherTestStack'))
