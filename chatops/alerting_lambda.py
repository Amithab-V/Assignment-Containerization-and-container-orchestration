import os
import json
import boto3
import requests

sns = boto3.client('sns')

def handler(event, context):
    slack_webhook = os.environ['SLACK_WEBHOOK_URL']
    msg = {
        "text": json.dumps(event, indent=2)
    }
    requests.post(slack_webhook, json=msg)
    return {
        'statusCode': 200,
        'body': 'Alert sent to Slack'
    }
