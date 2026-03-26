# Claude Code + SageMaker ML Demo

A demo showcasing Claude Code (powered by Bedrock Opus 4.6) running on a SageMaker Notebook instance, helping a Data Scientist build an ML model on the Titanic dataset.

## What It Does

Claude Code runs in the SageMaker terminal and autonomously writes and executes Python scripts for a complete ML workflow — data loading, exploration, feature engineering, model training, evaluation, and improvement.

## Prerequisites

- AWS Account with SageMaker, IAM, CloudFormation, and Bedrock permissions
- Bedrock model access enabled for **Claude Opus 4.6** (and optionally Haiku 3.5)

## Deploy

1. Enable Bedrock model access for Claude Opus 4.6 in your target region
2. Go to [CloudFormation Console](https://console.aws.amazon.com/cloudformation) → Create stack → Upload `cloudformation/template.yaml`
3. Stack name: `claude-sagemaker-demo`
4. Parameters: adjust `BedrockRegion` if needed (default: `us-east-1`)
5. Acknowledge IAM → Create stack
6. Wait ~8 minutes for `CREATE_COMPLETE`

## Run the Demo

1. SageMaker Console → Notebook instances → click "Open JupyterLab"
2. Open a Terminal (File → New → Terminal)
3. Run the one-time setup (~2-3 minutes):
   ```bash
   cd SageMaker
   bash setup_claude.sh
   ```
4. Start Claude Code:
   ```bash
   claude
   ```
5. Follow the prompts in `demo_prompts.md`

## Teardown

Delete the CloudFormation stack from the console. All resources are removed.

## Cost Estimate

| Resource | Estimated Cost |
|----------|---------------|
| SageMaker Notebook (`ml.t3.medium`) | ~$0.05/hour |
| Bedrock Opus 4.6 tokens | ~$15/M input, $75/M output |

Delete the stack after the demo to stop charges.

## Project Structure

```
├── cloudformation/
│   └── template.yaml       # CloudFormation template (deploy this)
├── demo_prompts.md          # Step-by-step prompts for the demo
├── docs/
│   └── presenter_guide.md   # Talking points and troubleshooting
└── README.md
```
