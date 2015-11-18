"""
Command line client for deploying CFN stacks via crassus
Usage:
    gaius --stack STACK --parameters PARAMETERS --topic-arn ARN [--region REGION]

Options:
  -h --help                Show this.
  --stack STACK            Stack Name.
  --parameters PARAMETERS  Parameters in format key=value[,key=value].
  --topic-arn ARN          The ARN of the notify topic.
  --region REGION          The region to deploy in. [default: eu-west-1]
"""

from gaius import crassus
from docopt import docopt


def send_message():
    arguments = docopt(__doc__)
    stack_name = arguments['--stack']
    parameters = arguments['--parameters']
    topic_arn = arguments['--topic-arn']
    region = arguments['--region']

    print crassus.notify_crassus(stack_name, parameters, topic_arn, region)
