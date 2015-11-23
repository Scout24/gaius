# -*- coding: utf-8 -*-
"""
Interface to the Crassus Lambda function. This module notifies Crassus
about updates to a CFN stack so Crassus will trigger the update process.
"""
import logging
import json

from boto3 import client

logger = logging.Logger('gaius')


def notify(stack_name, parameters, topic_arn, region):
    """ Sends an update notification to Crassus """
    message = generate_message(stack_name, parameters, region)
    sns_client = client('sns', region_name=region)
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
