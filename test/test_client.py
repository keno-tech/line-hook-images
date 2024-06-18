import json
from lambda_function import lambda_handler

event = {
    "body": json.dumps({
        "events": [
            {
                "message": {
                    "id": "text_message_id",
                    "type": "image",
                },
                "source": {
                    "userId": "test_user_id",
                }
            }
        ]
    })
}

context = {}
response = lambda_handler(event, context)
print(json.dumps(response, indent=2))