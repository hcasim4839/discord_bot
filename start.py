from discord import Intents, Client
from my_client import MyClient
from bot_utilities import get_secret, check_if_elapsed_time_passed
from datetime import datetime
import boto3
import json
'''
def test(name):
    if name == "acuity":
        return True
    else:
        return False
    
def upload_file(bucket_name, key, content):
    resource = boto3.resource('s3')
    bucket = resource.Bucket(bucket_name)
    content_encoded = content.encode('utf-8')

    bucket.put_object(Key= key, Body= content_encoded)
    #exception occurs if the file is not uploaded

bucket_name = "hf-ranked-search-specialties-id"
key = "specialties_id.json"

resource = boto3.resource('s3')
response = resource.Object(bucket_name,key)

data = response.get()['Body'].read().decode('utf-8')
data_dict = json.loads(data)



#formats the json file
file_content = json.dumps(data_dict, indent=2)
#the forward slash makes the previous word a folder
upload_file(bucket_name,'changes/loggedd.txt',f'User:Horacio\ndate:{datetime.now()}')
upload_file(bucket_name,"providence.json", file_content)

name1 = 'acuity'
name2 = '32'
dict = {
    "data": {
        "specialties": {
            "34234234": {
                "name": name1,
                "isRanked": test(name1)
            },
            "12": {
                "name": name2,
                "isRanked": test(name2)
            }
        }
    }
}


print(dict)
print(f'What to expect: {json.dumps(dict)}')'''

access_token_cache = {
}
client_secrets_cache = {
    'client_secret_spotify': None
}

intents = Intents.default()
intents.message_content = True

client = Client(intents=intents)

for key, value in client_secrets_cache.items():
    if value is None:
        secret = get_secret(key,'client_secret')    
        client_secrets_cache['client_secret_spotify'] = secret

if 'access_token_discord' in access_token_cache:
    has_elapsed_time_passed = check_if_elapsed_time_passed(access_token_cache.get('access_token_discord'), datetime.now(), 360)
    if has_elapsed_time_passed:
        token = get_secret('access_token_discord','access-token')
        access_token_cache['access_token_discord'] = token
    else:
        token = access_token_cache.get('access_token_discord')
else:
    token = get_secret('access_token_discord','access-token')
    access_token_cache['access_token_discord'] = token
print(token)
client = MyClient(client_secrets_cache, intents=intents)
client.run(token=token)