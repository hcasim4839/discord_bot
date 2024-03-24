import json

def return_response(status_code, json_body):
    response = {
        "statusCode": status_code,
        "body": json.dumps(json_body)
    }
    return response

def lambda_handler(event, context):
    try:
        return return_response(200, {
                "message": "Hello from Lambda!"
            })
    except Exception as e:
        return return_response(500, {"message": str(e)})