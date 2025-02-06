import requests

def connect_to_api_endpoint(method:str,url:str,query_params:dict=None,header_params:dict=None,data:dict=None):
    '''
    Generic function for major http methods

    Returns tuple; first is a status code if no exception occurs else a None
    second is the meta_data which could be response content or exception content
    
    first is response data or none; none if an exception occurs or if that is the data sent
    second is the status code or exception message
    '''
    try:
        response = requests.request(method=method,url=url,data=data,headers=header_params,params=query_params)
        print(f'The response: {response}')
        return response.json(), response.status_code
    except Exception as e:
        return None, e
    #need to change above tuple response to response, metadata where response
    #is the data or none if an error or non 200 occurs and the second should
    #be metadata aka status code or exception

    #will have to change all functions that call this function
