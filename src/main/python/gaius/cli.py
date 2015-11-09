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

    crassus.notify_crassus(stack_name, parameters, topic_arn, region)
