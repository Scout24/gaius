"""
Command line client for deploying CFN stacks via crassus
Usage:
    gaius --stack --parameters --topic-arn [--region]
Options:
  -h --help                Show this.
  --stack  Stack Name
  --parameters  Parameters in format....
  --topic-arn  The ARN of the notify topic
  --region  the region to deploy in[deafult: eu-west-1]
"""

from gaius import crassus
from docopt import docopt


def send_message():
    arguments = docopt(__doc__)
    stack_name = arguments['--stack']
    parameters = arguments['--parameters']
    topic_arn = arguments['--topic-arn']
    region = arguments['--region']

    crassus.notify_crassus(stack_name, parameters, topic_arn, region)
