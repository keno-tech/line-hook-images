# Memo

元々LINEからレシート画像を送付し、LambdaでS3の保管、
OCR(textract)による解析により、購入合計金額をSupabaseに保存する予定だった。

しかし、AWS textract が期待の結果ではなかった。
(金額は取得可能。しかし、どの金額が合計か、と結びつけることができないデータだった。)

この件は短工数を想定していたため、
LINE Webhook → AWS gateway + Lambda の仕組みを備忘録として残す。