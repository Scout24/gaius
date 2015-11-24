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


def parse_parameters(parameters):
    """ Parse input parameters from the command line. """
    parameter_list = [x for x in parameters.split(',')]
    return dict([y.split('=') for y in parameter_list])


def generate_message(stack_name, parameters, region, version=1):
    """ Generate the update notification message """
    message = {}
    message['version'] = version
    message['stackName'] = stack_name
    message['region'] = region
    message['parameters'] = parse_parameters(parameters)
    return message


def notify(stack_name, parameters, topic_arn, region):
    """ Sends an update notification to Crassus """
    message = generate_message(stack_name, parameters, region)
    sns_client = boto3.client('sns', region_name=region)
    json_answer = sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message),
    )
    logger.info(json_answer)


def receive(back_channel_name, poll_interval=10):
    """Reads out the back-channel on the deployment pipeline"""
    sqs_resource = boto3.resource('sqs')
    queue = sqs_resource.get_queue_by_name(QueueName=back_channel_name)
    while True:
        outer_message = queue.receive_messages(MaxNumberOfMessages=1)[0].body
        inner_message = json.loads(outer_message)['Message']
        message_dict = DeploymentResponse(**json.loads(inner_message))
        print(message_dict)
        sleep(poll_interval)
        break
