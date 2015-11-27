# -*- coding: utf-8 -*-
"""
Command line client for deploying CFN stacks via crassus
Usage:
    gaius --stack STACK --parameters PARAMETERS --topic-arn ARN
         [--region REGION] [--back-channel BACK_CHANNEL]

Options:
  -h --help                     Show this
  --stack STACK                 Stack Name
  --parameters PARAMETERS       Parameters in format key=value[,key=value]
  --topic-arn ARN               The ARN of the notify topic
  --region REGION               The region to deploy in [default: eu-west-1]
  --back-channel BACK_CHANNEL   The name of the back-channel AWS::SQS
                                from Crassus [default: crassus-output]
"""
import sys
from docopt import docopt

from . import service


def communicate():
    arguments = docopt(__doc__)
    stack_name = arguments['--stack']
    parameters = arguments['--parameters']
    topic_arn = arguments['--topic-arn']
    region = arguments['--region']
    back_channel_name = arguments['--back-channel']
    service.notify(stack_name, parameters, topic_arn, region)
    try:
        service.receive(back_channel_name, stack_name, region)
    except service.DeploymentErrorException:
        sys.exit(-1)
