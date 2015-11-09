"""
Command line client for deploying CFN stacks via crassus
Usage:
    gaius --stack --parameters --topic-arn [--region]
Options:
  -h --help                Show this.
  --stack  Stack Name
  --parameters  Parameters in format....
  --topic-arn  The ARN of the notify topic
  --region  the region to deploy in
"""

import json
from gaius.compat import OrderedDict
from gaius import crassus
from docopt import docopt

DEFAULT_REGION = 'eu-west-1'


def send_message():

    arguments = docopt(__doc__)
    stack_name = arguments['--stack']
    parameters = arguments['--parameters']
    topic_arn = arguments['--topic-arn']
    if '--region' in arguments:
        region = arguments['--region']
    else:
        region = DEFAULT_REGION

    message = transform_to_message_format(stack_name, parameters, region)
    crassus.notify_crassus(topic_arn, message, region)


def transform_to_message_format(stack_name, parameters, region):
    message = {}
    message['version'] = 1
    message['stackName'] = stack_name
    message['region'] = region

    parameter_list = [x for x in parameters.split(',')]
    parameter_dict = dict([y.split('=') for y in parameter_list])
    message['parameters'] = parameter_dict

    return json.dumps(OrderedDict(sorted(message.items())))
