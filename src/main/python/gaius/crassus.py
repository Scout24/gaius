# -*- coding: utf-8 -*-
from boto3 import client


def notify_crassus(topic_arn, message):
    sns_client = client("sns")
    json_str = sns_client.publish(
        TopicArn=topic_arn,
        Message=message
    )
    return json_str
