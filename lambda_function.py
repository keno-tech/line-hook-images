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

textract = boto3.client('textract', region_name='us-east-1')


def lambda_handler(event, context):
    try:
        # Parse the incoming LINE message event
        msg = json.loads(event['body'])
        
        # Process each event in the message
        for event in msg['events']:
            # Ensure the event is a message event
            if event['type'] == 'message' and event['message']['type'] == 'text':
                # Extract the reply token and user message text
                reply_token = event['replyToken']
                user_message = event['message']['text']
                
                # Reply to the user with the same text they sent
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text=user_message)
                )
        
        # Return a 200 response with the original message for logging/debugging purposes
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Messages processed successfully"})
        }
    except Exception as e:
        # Log the exception and return a 500 Internal Server Error response
        logger.error(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error"})
        }
