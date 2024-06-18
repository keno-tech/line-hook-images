# Lambdaの作成

1. AWS Management Consoleにログイン
2. Lambdaへ移動
3. 関数の作成ボタンを押下
4. 言語はPythonを選択し、関数の作成ボタンを押下

# S3バケットの作成

1. S3に移動
2. バケットの作成
3. バケット名やリージョン選択
4. バケットの作成ボタン押下

# LambdaのロールにS3アクセスを追加

1. Lambdaへ移動
2. 作成した関数へ移動
3. 設定タブへ移動し、実行ロールのアタッチされているロールを編集
4. AmazonS3FullAccessポリシーを選択し、追加する

# API Gatewayの作成

1. API Gatewayサービスに移動
2. HTTP API欄から構築ボタンを押下
3. 統合欄をLambdaを選択し、リージョン、関数名、Version(2.0)を設定し、
   API名を入力し、次へ
4. メソッドはPOSTで次へ
5. 他は全て進んでください

# IAMポリシー(例)

```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "AllowTextractAccess",
			"Effect": "Allow",
			"Action": [
				"textract:AnalyzeDocument",
				"textract:DetectDocumentText"
			],
			"Resource": [
				"*"
			]
		},
		{
			"Sid": "AllowS3Access",
			"Effect": "Allow",
			"Action": [
				"s3:GetObject",
				"s3:PutObject",
				"s3:ListBucket"
			],
			"Resource": [
				"arn:aws:s3:::py-lambda-receipts-bucket",
				"arn:aws:s3:::py-lambda-receipts-bucket/receipts/*"
			]
		},
	]
}
```

# ローカルのaws設定(リージョン)の変更

```bash
aws configure set region us-east-1
aws configure set region ap-northeast-1
```

# AWS Textractの疎通確認

```bash
aws textract analyze-document --document '{"S3Object":{"Bucket":"[バケット名] ","Name":"[イメージ画像]"}}' --feature-types 'FORMS' --region [リージョン名]
```


# URL

https://qiita.com/n_oshiumi/items/53d0ad1d95c9c11aa2fd#amazon-textract