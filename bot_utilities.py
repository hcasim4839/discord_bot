# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

import boto3
from botocore.exceptions import ClientError
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()
server_url = os.getenv("ServerEndpoint")

def get_secret(secret_key, secret_name):
    '''
    Connects to aws secret manager
        Returns:
            String

    '''
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret_dict = json.loads(get_secret_value_response['SecretString'])


    return secret_dict.get(secret_key)

def start_server(game_name):
    '''
    Connects to aws lambda function

        Returns:    
            A status code with json response otherise Exception class and exception message if exception occured
            
    '''
    try:
        url = f"{server_url}"

        json_request = {
            "gameName": game_name
        }

        response = requests.post(url,json_request)
        json_message = response.json()

        if response.status_code == 200:
            return response.status_code, json_message
        else:
            return response.status_code, json_message
    except Exception as e:
        exception_message = str(e)
        return Exception, exception_message