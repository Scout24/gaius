# -*- coding: utf-8 -*-
from unittest import TestCase
from gaius.crassus import notify_crassus, transform_to_message_format
import boto3
import os
from moto import mock_sns

# Else we run into problems with mocking
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['no_proxy'] = ''


class CrassusTests(TestCase):

    def setUp(self):
        self.my_mock_sns = mock_sns()
        self.my_mock_sns.start()
        self.sns = boto3.resource('sns', region_name='eu-west-1')
        self.topic = self.sns.create_topic(Name='test_sns')

    def tearDown(self):
        self.my_mock_sns.stop()

    def test_notify_crassus(self):
        response = notify_crassus(
            stack_name='sample-stack',
            parameters='parameter1=value1,parameter2=value2',
            topic_arn=self.topic.arn, region='eu-west-1')
        self.assertEquals(response['ResponseMetadata']['HTTPStatusCode'], 200)

    def test_should_transform_parameters_to_message(self):
        stack_name = 'sample-stack'
        parameters = 'parameter1=value1,parameter2=value2'
        region = 'eu-west-1'

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

        message = transform_to_message_format(
            stack_name, parameters, region)
        self.assertEquals(message, expected_message)
