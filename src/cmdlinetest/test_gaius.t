#!/usr/bin/env cram
# vim: set syntax=cram :

# These are the cram tests for the gaius.

# Test help

  $ gaius -h
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
# Test failing @ wrong parametrization

  $ gaius --stack some_stack --topic-arn arn:aws:sns:eu-west-1::topic
  Usage:
      gaius --stack STACK --parameters PARAMETERS --topic-arn ARN
           [--region REGION] [--back-channel BACK_CHANNEL]
  [1]
