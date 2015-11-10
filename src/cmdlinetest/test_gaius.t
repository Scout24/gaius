#!/usr/bin/env cram
# vim: set syntax=cram :

# These are the cram tests for the gaius.

# Test help

  $ gaius -h
  Command line client for deploying CFN stacks via crassus
  Usage:
      gaius --stack STACK --parameters PARAMETERS --topic-arn ARN [--region REGION]
  
  Options:
    -h --help                Show this.
    --stack STACK  Stack Name
    --parameters PARAMETERS  Parameters in format key=value[,key=value]
    --topic-arn ARN  The ARN of the notify topic
    --region REGION  the region to deploy in [default: eu-west-1]

# Test failing @ wrong parametrization

  $ gaius --stack some_stack --topic-arn arn:aws:sns:eu-west-1::topic
  Usage:
      gaius --stack STACK --parameters PARAMETERS --topic-arn ARN [--region REGION]
  [1]