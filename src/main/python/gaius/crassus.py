"""
Interface to the Crassus Lambda function. This module notifies Crassus
about updates to a CFN stack so Crassus will trigger the update process.
"""
# -*- coding: utf-8 -*-
from boto3 import client


def notify_crassus(topic_arn, message, region_name='eu-west-1'):
    sns_client = client('sns', region_name=region_name)
    json_str = sns_client.publish(
        TopicArn=topic_arn,
        Message=message
    )
    return json_str
