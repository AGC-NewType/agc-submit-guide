import os
import json
from urllib import request

os.environ['REST_URL']='10.0.4.250'

# # URL
url = 'http://'+ os.environ['REST_URL'] + ':30000/test'
# # headers
headers = {
    "Content-Type": "application/json"
}

# data
temp = {
    "color": "black",
    "size": 200
}

data = json.dumps(temp).encode('utf8')
req =  request.Request(url, data=data, headers=headers) # this will make the method "POST"
resp = request.urlopen(req)
print(resp.read().decode('utf8'))
print(resp.read().decode('utf8'))