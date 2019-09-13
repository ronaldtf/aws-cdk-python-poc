#!/usr/bin/env python3

__author__ = 'Ronald T. Fernandez (Ronald Teijeira Fernandez)'
__email__ = 'ronaldtfernandez@gmail.com'
__version__ = '1.0'
__date__ = 'September 2019'

from aws_cdk import core
from serverless.serverless_stack import ServerlessStack

if __name__ == "__main__":    
    app = core.App()
    ServerlessStack(app, "serverless")
    app.synth()
