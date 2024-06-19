import json
import boto3
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
import os
from dotenv import load_dotenv

load_dotenv()

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

s3_bucket_name = os.getenv('S3_BUCKET_NAME')


def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(msg, indent=2))

        msg = json.loads(event['body'])

        for event in msg.get('events', []):
            # Ensure the event is a message event
            if event['type'] == 'message':
                event_type = event['message']['type']
                s3 = boto3.client('s3')
                message_content = line_bot_api.get_message_content(event['message']['id'])
                print("Message Content:", json.dumps(msg, indent=2)) 
                data = message_content.content

                if event_type == 'image':
                    object_key = f'{event["message"]["id"]}.jpg'
                    s3.put_object(Bucket=s3_bucket_name, Key=object_key, Body=data)
                    print(f"Image uploaded to S3: {s3_bucket_name}/{object_key}")

                elif event_type == 'video':
                    pass


        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Messages processed successfully"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"{e}"})
        }
