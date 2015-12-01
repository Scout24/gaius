[![Build Status](https://travis-ci.org/ImmobilienScout24/gaius.svg)](https://travis-ci.org/ImmobilienScout24/gaius)
[![Code Health](https://landscape.io/github/ImmobilienScout24/gaius/master/landscape.svg?style=flat)](https://landscape.io/github/ImmobilienScout24/gaius/master)
[![Coverage Status](https://coveralls.io/repos/ImmobilienScout24/gaius/badge.svg?branch=master&service=github)](https://coveralls.io/github/ImmobilienScout24/gaius?branch=master)
# gaius
Gaius, the deployment client that triggers [crassus](https://github.com/ImmobilienScout24/crassus)  to deploy artefacts

```
Command line client for deploying CFN stacks via crassus
Usage:
    gaius --stack STACK --parameters PARAMETERS --trigger-channel TOPIC_ARN
         [--region REGION] --back-channel QUEUE_URL [--timeout TIMEOUT]

Options:
  -h --help                     Show this
  --stack STACK                 Stack Name
  --parameters PARAMETERS       Parameters in format key=value[,key=value]
  --trigger-channel TOPIC_ARN   The ARN of the notify topic
  --region REGION               The region to deploy in [default: eu-west-1]
  --back-channel QUEUE_URL      The URL of the back-channel AWS::SQS
                                from Crassus
  --timeout TIMEOUT             Timeout in seconds after that gaius stops
                                polling on back channel and returns
                                [default: 600]
```