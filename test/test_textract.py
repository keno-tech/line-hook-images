import boto3

def test_textract_connection():
    try:
        # テスト用のリージョン名
        region_name = "us-east-1"
        # テスト用のS3バケットとドキュメントID
        test_bucket = "py-lambda-receipts-bucket"  # 任意
        test_document = "513055908901945347.jpg"   # 任意
        
        # Textractクライアントの設定
        textract = boto3.client('textract', region_name=region_name)
        
        # Textractエンドポイントへの接続テスト
        response = textract.analyze_document(
            Document={'S3Object': {'Bucket': test_bucket, 'Name': test_document}},
            FeatureTypes=["FORMS"]
        )

        print("Textract connection test succeeded.")
        print(response)

    except Exception as e:
        print(f"Textract connection error: {e}")

# テスト実行
test_textract_connection()
