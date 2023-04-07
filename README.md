# Slack Payroll Notification Bot
This AWS Lambda function sends a notification to a Slack channel with the current week's payroll information. It also toggles an AWS EventBridge scheduler on and off.


## Functionality

1. If triggered by an AWS EventBridge scheduler with a matching domain name (as specified by the "lookid" environment variable), the function turns off the scheduler and prints a message to the console.

2. If triggered by any other means, the function reads the current week's payroll information from a Google Sheet (as specified by the "gsheetid" environment variable) and formats a message payload to send to a Slack webhook (as specified by the "webhook" environment variable). The payload includes the following information:
  *Work week and dates
  *Total hours worked
  *Total pay received
  *Link to the Google Sheet
  *Button to mark payment as complete
  *The function sends the payload to the Slack webhook and prints a message to the console.
3. The function turns on an AWS EventBridge scheduler to trigger the function again in 15 minutes.
4. The function turns on an AWS EventBridge scheduler to trigger the function again in 15 minutes.

## Requirements
*Python 3.x
*AWS CLI
*An AWS account with sufficient permissions to create and manage Lambda functions, IAM roles, EventBridge schedulers, and CloudWatch Logs.
*A Slack account with sufficient permissions to create and manage webhooks.

## Setup
1. Clone or download the code repository.
2. Create a virtual environment for the project, activate it, and install the required packages:
3. Create an IAM role for the Lambda function with the following permissions:
  *AWSLambdaBasicExecutionRole
  *AmazonSSMReadOnlyAccess
  *AmazonEventBridgeFullAccess
  *CloudWatchLogsFullAccess
  *AmazonS3FullAccess (if using S3 to store the code package)
4. Create a Slack webhook and copy its URL.
5. Create a Google Sheet and share it with the service account associated with the IAM role created in step 3.
6. Create an AWS EventBridge scheduler with a cron expression of cron(*/15 * * * ? *) and a target of this Lambda function. Set the name of the scheduler to payalert_reminder.
7. Create an S3 bucket (optional) and upload the code package to it:
8. Create the Lambda function with the following settings:
  *Runtime: Python 3.x
  *Handler: lambda_function.lambda_handler
  *Role: the IAM role created in step 3
  *Code source: either an S3 bucket or a ZIP file (if using the former, enter the S3 URL in the "Code source" field; if using the latter, upload the ZIP file directly)
  *Environment variables:
    * 'gsheetid': the ID of the Google Sheet (found in the URL)
    *'webhook': the URL of the Slack webhook
    *'lookid': the domain name to match with the AWS EventBridge scheduler (optional)
  *Timeout: 1 minute (recommended)
  *Memory: 128 MB (minimum)
 9. Test the function by triggering it manually from the Lambda console or the AWS CLI:

  




