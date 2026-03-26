# Presenter Guide: Claude Code + SageMaker Demo

## Overview

This demo shows Claude Code (powered by Bedrock Opus 4.6) running directly on a SageMaker Notebook instance, helping a Data Scientist build an ML model on the Titanic dataset. Claude Code writes and executes Python scripts autonomously from the terminal.

## Prerequisites Checklist

- [ ] AWS Account with SageMaker, IAM, CloudFormation, and Bedrock permissions
- [ ] Bedrock model access enabled for Claude Opus 4.6 in your region
- [ ] CloudFormation stack deployed (`cloudformation/template.yaml`)

## Setup (~10 minutes)

1. Enable Bedrock model access for Claude Opus 4.6 (and Haiku 3.5 for fast model) in your region
2. Deploy the CloudFormation stack — upload `cloudformation/template.yaml`
3. Wait for `CREATE_COMPLETE` (~5 minutes)
4. Go to SageMaker Console → Notebook instances → click "Open JupyterLab"
5. In JupyterLab, open a Terminal (File → New → Terminal)
6. Run the one-time setup (~2-3 minutes):
   ```bash
   cd SageMaker
   bash setup_claude.sh
   ```
7. Then start Claude Code:
   ```bash
   claude
   ```
8. Claude Code should start and show the Opus 4.6 model. You're ready.

## Demo Flow (~25 minutes)

You type natural language prompts into Claude Code's terminal. It writes Python scripts, creates files, and runs them — all autonomously.

### Step 1: Data Loading (3 min)

Type into Claude Code:
> Load the Titanic dataset from ./data/titanic.csv with pandas. Show the first 10 rows, shape, and column types.

**Talking point:** Claude Code generates correct pandas code and runs it immediately. No copy-paste, no switching windows.

### Step 2: Data Exploration (4 min)

> Generate summary statistics and create visualizations showing the distribution of Age, Fare, Pclass, and Survived. Save plots to plots/exploration.png.

**Talking point:** Claude Code picks appropriate chart types, uses seaborn/matplotlib, and saves output files.

### Step 3: Missing Value Analysis (3 min)

> Analyze missing values in the dataset. Show which columns have missing data, percentage missing, and suggest imputation strategies.

**Talking point:** Claude Code explains *why* each strategy works — it's a thought partner, not just a code generator.

### Step 4: Feature Engineering (4 min)

> Suggest and implement feature transformations — extract titles from names, create family size, encode categoricals. Save processed data to data/titanic_processed.csv.

**Talking point:** This is where Claude Code shines — domain knowledge + non-trivial transformations.

### Step 5: Model Training (3 min)

> Train a Random Forest classifier on the processed data with proper train-test split. Print training accuracy.

**Talking point:** Claude Code includes train-test splitting automatically — best practice baked in.

### Step 6: Model Evaluation (4 min)

> Evaluate the model with classification metrics and a confusion matrix. Save the confusion matrix plot.

**Talking point:** Walk through metrics briefly. The confusion matrix makes performance tangible.

### Step 7: Model Improvement (4 min)

> Suggest and implement hyperparameter tuning with GridSearchCV. Compare tuned vs baseline performance.

**Talking point:** Claude Code suggests concrete improvements and explains trade-offs.

## Key Messages

- Claude Code on Bedrock Opus 4.6 accelerates the entire ML workflow
- Runs directly on SageMaker — data never leaves your AWS account
- Writes AND executes code autonomously — fully agentic
- Understands ML context and generates production-quality code

## Troubleshooting

**Q: Claude Code says "model not found"**
A: Verify Bedrock model access is enabled for Claude Opus 4.6 in your region. Check the Bedrock Console → Model access.

**Q: Claude Code won't start**
A: Run `source ~/.claude_code_env` first, then `claude`. If Node.js isn't found, the lifecycle config may have timed out — check CloudWatch Logs.

**Q: Dataset not found**
A: Run manually:
```bash
mkdir -p data && wget -q "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv" -O data/titanic.csv
```

**Q: Claude Code generates an error**
A: Just tell it "fix the error" — this demonstrates its debugging capability.

## Teardown

Delete the CloudFormation stack from the console. This removes the notebook instance, IAM role, and lifecycle config.
