#!/usr/bin/env cram
# vim: set syntax=cram :

# These are the cram tests for the gaius.

# Test help

  $ gaius -h
  Command line client for deploying CFN stacks via crassus
  Usage:
      gaius --stack STACK --parameters PARAMETERS --trigger-channel TOPIC_ARN
           [--region REGION] [--back-channel SQS_NAME] [--timeout TIMEOUT]
  
  Options:
    -h --help                     Show this
    --stack STACK                 Stack Name
    --parameters PARAMETERS       Parameters in format key=value[,key=value]
    --trigger-channel TOPIC_ARN   The ARN of the notify topic
    --region REGION               The region to deploy in [default: eu-west-1]
    --back-channel SQS_NAME       The name of the back-channel AWS::SQS
                                  from Crassus [default: crassus-output]
    --timeout TIMEOUT             Timeout in seconds after that gaius stops
                                  polling on back channel and returns
                                  [default: 600]
#Test failing @ wrong parametrization

  $ gaius --stack some_stack --topic-arn arn:aws:sns:eu-west-1::topic
  Usage:
      gaius --stack STACK --parameters PARAMETERS --trigger-channel TOPIC_ARN
           [--region REGION] [--back-channel SQS_NAME] [--timeout TIMEOUT]
  [1]
