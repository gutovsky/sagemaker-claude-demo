#!/usr/bin/env python3
import aws_cdk as cdk

from stacks.demo_stack import DemoStack

app = cdk.App()
DemoStack(app, "SageMakerAiAgentDemo")
app.synth()
