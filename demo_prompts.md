# Demo Prompts for Claude Code on SageMaker

Open JupyterLab Terminal → `cd SageMaker` → `claude`

Then use these prompts in order:

## Step 1: Data Loading
> Load the Titanic dataset from ./data/titanic.csv with pandas. Show the first 10 rows, shape, and column types.

## Step 2: Data Exploration
> Generate summary statistics and create visualizations showing the distribution of Age, Fare, Pclass, and Survived. Save plots to plots/exploration.png.

## Step 3: Missing Value Analysis
> Analyze missing values in the dataset. Show which columns have missing data, percentage missing, and suggest imputation strategies.

## Step 4: Feature Engineering
> Suggest and implement feature transformations — extract titles from names, create family size, encode categoricals. Save processed data to data/titanic_processed.csv.

## Step 5: Model Training
> Train a Random Forest classifier using a SageMaker Training Job on a separate ml.m5.large instance. Upload the processed data to S3, create a training script, launch the job, and stream the logs. Print training accuracy when done.

## Step 6: Model Evaluation
> Download the trained model artifact from S3 (from the training job in the previous step). Load it locally, run predictions on the test set, and evaluate with classification metrics and a confusion matrix. Save the confusion matrix plot to plots/confusion_matrix.png.

## Step 7: Model Improvement
> Suggest and implement hyperparameter tuning with GridSearchCV. Compare tuned vs baseline performance.

## Step 8: Build & Save the Final Model
> Build the final production-ready model using the best hyperparameters. Save it as a serialized artifact using joblib to models/titanic_model.joblib. Also save the preprocessing pipeline so the model can be loaded and used for inference on new data. Print a summary of the final model's performance.
