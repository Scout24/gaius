"""
Command line client for deploying CFN stacks via crassus
Usage:
    gaius --stack STACK --parameters PARAMETERS --topic-arn ARN [--region REGION] [--back-channel BACK_CHANNEL]

Options:
  -h --help                     Show this.
  --stack STACK                 Stack Name
  --parameters PARAMETERS       Parameters in format key=value[,key=value]
  --topic-arn ARN               The ARN of the notify topic to Crassus
  --region REGION               The region to deploy in [default: eu-west-1]
  --back-channel BACK_CHANNEL   The name of the back-channel AWS::SQS from Crassus [default: crassus-output]
"""

from gaius import crassus, back_channel
from docopt import docopt


def send_message():
    arguments = docopt(__doc__)
    stack_name = arguments['--stack']
    parameters = arguments['--parameters']
    topic_arn = arguments['--topic-arn']
    region = arguments['--region']
    back_channel_name = arguments['--back-channel']

    print crassus.notify_crassus(stack_name, parameters, topic_arn, region)
    back_channel.receive_messages(back_channel_name)
