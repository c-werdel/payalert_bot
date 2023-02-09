import urllib3
import pandas as pd
import json
import os
import boto3

http = urllib3.PoolManager()

gsheetid = os.environ["gsheetid"]

def mydoc():
	sheet_name = "Sheet1"

	gsheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, sheet_name)
	df = pd.read_csv(gsheet_url)

	current_week = (df.loc[0])

	for i in df.index:
		if df.loc[i]['Total Pay'] == None:
			raise Exception("Something went wrong in parsing the Pandas from Excel sheet!")

		if not pd.isna(df.loc[i]['Total Pay']):
			current_week = df.loc[i]

	if current_week['Total Pay'] == "$0.00":
		print("NO MONEY!")
	print("FOUND CURRENT WEEK!")
	return current_week
	
def lambda_handler(event, context):
	worked = False
	lookid = os.environ["lookid"]

	try: 
		api_event = event['requestContext']['domainName']
		if api_event == lookid:
				worked = True
	except:
		pass

	if worked:
		client = boto3.client('scheduler',  region_name='us-east-1')
		response = client.update_schedule(
	    FlexibleTimeWindow={
	        'Mode': 'OFF'
	    },
	    Name='payalert_reminder', 
	    ScheduleExpression='cron(*/15 * * * ? *)',
	    State='DISABLED',
	    Target= {
	        'Arn': 'arn:aws:lambda:us-east-1:297098627551:function:Slack_payroll_notification',
	        'RoleArn': 'arn:aws:iam::297098627551:role/service-role/Amazon_EventBridge_Scheduler_LAMBDA_payalert_reminder_a330188cab'
	    }
	)
	else: 
		current_week = mydoc()
		work_week = current_week['Work Week']
		Dates = current_week['Dates']
		Total_Hours = current_week['Total Hours']
		Total_Pay = current_week['Total Pay']

		hook_url = os.environ["webhook"]                   
		payload = {	
			"blocks": [
				{
					"type": "header",
					"text": {
						"type": "plain_text",
						"text": "Pay Roll Alert\n"
					}
				},
				{
					"type": "section",
					"fields": [
						{
						"type": "mrkdwn",
						"text": "For Connor Werdel"
					}
					]
				},
				{
					"type": "section",
					"fields": [
						{
							"type": "mrkdwn",
							"text": f"*Work Week:*\n {work_week} {Dates}"
						}
					]
				},
				{
					"type": "section",
					"fields": [
						{
							"type": "mrkdwn",
							"text": f"*Total Hours: *\n {Total_Hours}"
						}
					]
				},
				{
					"type": "section",
					"fields": [
						{
							"type": "mrkdwn",
							"text": f"*Paid Amount:*\n{Total_Pay}"
						}
					]
				},
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": f"*Pay Roll Sheet:*\n<https://docs.google.com/spreadsheets/d/{gsheetid}/edit#gid=1445946700|Link>"
					}
				},
				{
				"type": "actions",
				"block_id": "actionblock789",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Payment complete"
						},
						"style": "primary",
						"value": "click_me_123"
					}             
				]            
				}
			]
		}
	
		encoded_data = json.dumps(payload).encode('utf-8')
		r = http.request( 
			'POST',
			hook_url,
			body=encoded_data,
			headers={'Content-Type': 'application/json'})
	
		client = boto3.client('scheduler',  region_name='us-east-1')
		response = client.update_schedule(
		    FlexibleTimeWindow={
		        'Mode': 'OFF'
		    },
		    Name='payalert_reminder', 
		    ScheduleExpression='cron(*/15 * * * ? *)',
		    State='ENABLED',
		    Target= {
		        'Arn': 'arn:aws:lambda:us-east-1:297098627551:function:Slack_payroll_notification',
		        'RoleArn': 'arn:aws:iam::297098627551:role/service-role/Amazon_EventBridge_Scheduler_LAMBDA_payalert_reminder_a330188cab'
		    }
		)

if __name__ == "__main__":
	lambda_handler(None, None)
