import json
import boto3
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
import os
from dotenv import load_dotenv

# 環境変数のロード
load_dotenv()

# LINE Bot APIの設定
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
s3_bucket_name = os.getenv('S3_BUCKET_NAME')

# Textractクライアントの設定
# Amazon Textractは日本語対応しておらず、限られたリージョンでしか使用できない。
# その為、us-east-1(米国東部 (バージニア北部))を使用する。
textract = boto3.client('textract', region_name='us-east-1')

def extract_receipt_data(bucket_name, object_key):
    print(f"Extracting receipt data from {bucket_name}/{object_key}")
    response = textract.analyze_document(
        Document={'S3Object': {'Bucket': bucket_name, 'Name': object_key}},
        FeatureTypes=["FORMS"]
    )

    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text = block['Text']
            print(f"Detected text: {text}")

def lambda_handler(event, context):
    try:
        print("Received event: " + json.dumps(event, indent=2))

        body = json.loads(event['body'])
        print("Parsed body: " + json.dumps(body, indent=2))

        for evt in body.get('events', []):
            print(f"Processing event: {json.dumps(evt, indent=2)}")
            if evt['type'] == 'message' and evt['message']['type'] == 'image':
                message_content = line_bot_api.get_message_content(evt['message']['id'])
                image_data = message_content.content
                print(f"Received image data: {len(image_data)} bytes")

                s3 = boto3.client('s3')
                bucket_name = s3_bucket_name
                object_key = f'receipts/{evt["message"]["id"]}.jpg'
                s3.put_object(Bucket=bucket_name, Key=object_key, Body=image_data)
                print(f"Image uploaded to S3: {bucket_name}/{object_key}")

                extract_receipt_data(bucket_name, object_key)

                line_bot_api.reply_message(
                    evt['replyToken'],
                    TextSendMessage(text='レシートが処理されました。')
                )
                print("Reply message sent")

        return {
            'statusCode': 200,
            'body': json.dumps('Image received and data stored.')
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
