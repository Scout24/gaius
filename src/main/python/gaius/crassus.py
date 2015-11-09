"""
Interface to the Crassus Lambda function. This module notifies Crassus
about updates to a CFN stack so Crassus will trigger the update process.
"""
# -*- coding: utf-8 -*-
from boto3 import client
import json
from gaius.compat import OrderedDict

CRASSUS_MESSAGE_VERSION = 1


def notify_crassus(stack_name, parameters, topic_arn, region):
    """ Sends an update notification to Crassus """
    message = transform_to_message_format(stack_name, parameters, region)
    sns_client = client('sns', region_name=region)
    json_str = sns_client.publish(
        TopicArn=topic_arn,
        Message=message
    )
    return json_str


def transform_to_message_format(stack_name, parameters, region):
    message = {}
    message['version'] = CRASSUS_MESSAGE_VERSION
    message['stackName'] = stack_name
    message['region'] = region

    parameter_list = [x for x in parameters.split(',')]
    parameter_dict = dict([y.split('=') for y in parameter_list])
    message['parameters'] = parameter_dict

    return json.dumps(OrderedDict(sorted(message.items())))
