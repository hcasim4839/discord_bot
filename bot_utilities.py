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
import datetime
from table2ascii import table2ascii

load_dotenv()
server_url = "https://q19me3z8id.execute-api.us-east-1.amazonaws.com/Prod"
secret_dict_cache = []
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
        url = ''

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

def check_if_elapsed_time_passed(start_time:datetime.datetime, end_time:datetime.datetime, timeout_duration:int) -> bool:
    '''
    Checks if x amount of time passed given a start and endtime with datetime datatype

    Returns:
        bool: Whether the sufficient time has passed
    '''
    time_passed = end_time - start_time
    has_sufficient_time_passed = time_passed >= datetime.timedelta(minutes=timeout_duration)

    return has_sufficient_time_passed

def create_ascii_table(amt_of_rows, row_list, column_width = None, cell_alignment_list = None, header_list = None):
    table = None
    table_body = []
    for index in range(amt_of_rows):
        new_row_data = row_list[index]
        table_body.append(new_row_data)
    

    table = table2ascii(body=table_body,header=header_list, cell_padding=2)
    return table

async def insert_reactions_to_message(message, reaction_list):
    for reaction in reaction_list:
        await message.add_reaction(f'{reaction}')

    return message

def connect_to_api_endpoint(http_method, url, header_dict=None, query_parameters_dict=None, path_parameter_dict=None,data=None):
    try:
        print()
        result = requests.request(method=http_method, url=url,data=data, headers = header_dict, params = query_parameters_dict)
        return result.json()

    except Exception as e:
        exception_message = str(e)
        return Exception, exception_message