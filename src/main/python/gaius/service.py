# -*- coding: utf-8 -*-
"""
Interface to the Crassus Lambda function. This module notifies Crassus
about updates to a CFN stack so Crassus will trigger the update process.
"""

import sys
import json
import logging
from time import sleep

import boto3

logger = logging.getLogger('gaius')
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

FINAL_STATES = [
    'CREATE_FAILED',
    'CREATE_COMPLETE',
    'ROLLBACK_FAILED',
    'ROLLBACK_COMPLETE',
    'DELETE_FAILED',
    'DELETE_COMPLETE',
    'UPDATE_COMPLETE',
    'UPDATE_ROLLBACK_FAILED',
    'UPDATE_ROLLBACK_COMPLETE'
]


def parse_parameters(parameters):
    """ Parse input parameters from the command line """
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
    logger.debug(json_answer)


def receive(back_channel_name, poll_interval=2, num_attempts=60):
    """Reads out the back-channel on the deployment pipeline"""
    original_num_attempts = num_attempts
    sqs_resource = boto3.resource('sqs')
    queue = sqs_resource.get_queue_by_name(QueueName=back_channel_name)
    while num_attempts > 0:
        messages = queue.receive_messages(MaxNumberOfMessages=1)
        if not messages:
            num_attempts -= 1
        else:
            message = messages[0]
            message_dict = json.loads(message.body)
            message.delete()
            logger.debug(message_dict)
            logger.info('%s: %s',
                        message_dict['status'], message_dict['message'])
            if message_dict['status'] == 'failure':
                logger.info('Final Crassus message received')
                return
            elif (message_dict['resourceType'] == 'AWS::CloudFormation::Stack'
                  and message_dict['status'] in FINAL_STATES):
                logger.info('Final CFN message received')
                return
            num_attempts = original_num_attempts
        sleep(poll_interval)
    logger.info('No final CFN message was received')
