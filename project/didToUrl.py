from urllib.error import HTTPError
def convert_to_url(did):
    did=did
    convertedDid=did.replace(':', '/')
    convertedDid=convertedDid.replace('%A3',':')
    convertedDid=convertedDid[7:]
    convertedDid=convertedDid+'/did.json'
    convertedDid="http:/"+convertedDid
    url=convertedDid
    print ("The requested URL is "+ url)
    return url

def ret_did_method():
    did_method='did:web'
    return did_method

def ret_method_specific_id(did):
    did=did
    convertedDid=did.replace(':', '/')
    convertedDid=convertedDid.replace('%A3',':')
    methodSpecificId=convertedDid[7:]
    return methodSpecificId

# #extracts a dictionary from the did given a url
# def extract_json(url):
#     try:
#         r=requests.get(url)
#         #get the request in dict type
#         decodedJson_dict=r.json()
#         #return a dictionary with the did values
#         return decodedJson_dict
        
#     except HTTPError as http_err:
#         print(f'HTTP error occurred: {http_err}')
#     except Exception as err:
#         print(f'Other error occurred: {err}')





did="did:web:127.0.0.1%A35000:email3:doc12"
print(convert_to_url(did))
