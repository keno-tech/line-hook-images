import json
import boto3
from linebot import LineBotApi, WebhookHandler
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

s3 = boto3.client('s3')
s3_bucket_name = os.getenv('S3_BUCKET_NAME')

def lambda_handler(event, context):
    try:
        # Parse the incoming LINE message event
        msg = json.loads(event['body'])
        print("Received event:", json.dumps(msg, indent=2))

        for event in msg.get('events', []):
            # Ensure the event is a message event
            if event['type'] == 'message':
                message_type = event['message']['type']
                message_id = event['message']['id']
                
                # Get message content from LINE
                message_content = line_bot_api.get_message_content(message_id)
                
                # Get the current date and time
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                
                # Determine the type of message and handle accordingly
                if message_type == 'image':
                    object_key = f'{timestamp}_{message_id}.jpg'
                    data = message_content.content
                    try:
                        s3.put_object(Bucket=s3_bucket_name, Key=object_key, Body=data)
                        print(f"Image uploaded to S3: s3://{s3_bucket_name}/{object_key}")
                    except Exception as e:
                        print(f"Error uploading image to S3: {e}")
                    
                elif message_type == 'video':
                    # Handle video messages if needed
                    object_key = f'{timestamp}_{message_id}.mp4'
                    data = message_content.content
                    print("Trying to upload", s3_bucket_name, object_key)
                    try:
                        s3.put_object(Bucket=s3_bucket_name, Key=object_key, Body=data)
                        print(f"Video uploaded to S3: s3://{s3_bucket_name}/{object_key}")
                    except Exception as e:
                        print(f"Error uploading video to S3: {e}")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Messages processed successfully"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }
