"""
Reads out the back-channel on the deployment pipeline. We will receive
messages from Crassus (as well as CloudFormation later).
"""
import boto3
import json
from time import sleep
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping


def receive_messages(back_channel_name, poll_interval=10):
    sqs_resource = boto3.resource('sqs')
    queue = sqs_resource.get_queue_by_name(QueueName=back_channel_name)

    while True:
        message = queue.receive_messages(MaxNumberOfMessages=1)
        message_dict = handle_message(message)
        print(message_dict)
        sleep(poll_interval)


def handle_message(message):
    message_obj = json.loads(message)
    message_dict = Message(message_obj['Message'])

    return message_dict


class Message(Mapping):

    def __init__(self, payload):
        message_rows = [x for x in payload.split('\n')]
        self.data = dict([y.split('=') for y in message_rows])

    def __getitem__(self, key):
        return self.data[key]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __str__(self):
        if (self.data['ResourceStatusReason']):
            return 'Stack: {0}, Resource: {1}, Status: {2}, Reason: "{3}"'.format(
                self.data['StackName'],
                self.data['LogicalResourceId'],
                self.data['ResourceStatus'],
                self.data['ResourceStatusReason'])
        else:
            return "Stack: {0}, Resource: {1}, Status: {2}".format(
                self.data['StackName'],
                self.data['LogicalResourceId'],
                self.data['ResourceStatus'])

    def __repr__(self):
        repr(self.data)
