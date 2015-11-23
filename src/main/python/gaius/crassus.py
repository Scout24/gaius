# -*- coding: utf-8 -*-
"""
Interface to the Crassus Lambda function. This module notifies Crassus
about updates to a CFN stack so Crassus will trigger the update process.
"""
import json
import logging
from time import sleep

import boto3

from .message import DeploymentResponse

logger = logging.Logger('gaius')


def notify(stack_name, parameters, topic_arn, region):
    """ Sends an update notification to Crassus """
    message = generate_message(stack_name, parameters, region)
    sns_client = boto3.client('sns', region_name=region)
    json_answer = sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message),
    )
    logger.info(json_answer)


def generate_message(stack_name, parameters, region, version=1):
    message = {}
    message['version'] = version
    message['stackName'] = stack_name
    message['region'] = region
    parameter_list = [x for x in parameters.split(',')]
    parameter_dict = dict([y.split('=') for y in parameter_list])
    message['parameters'] = parameter_dict
    return message


def receive(back_channel_name, poll_interval=10):
    """Reads out the back-channel on the deployment pipeline"""
    sqs_resource = boto3.resource('sqs')
    queue = sqs_resource.get_queue_by_name(QueueName=back_channel_name)
    while True:
        message = queue.receive_messages(MaxNumberOfMessages=1)
        message_dict = DeploymentResponse(**json.loads(message))
        print(message_dict)
        sleep(poll_interval)
