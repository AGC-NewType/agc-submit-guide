import os
import json
from urllib import request

# # URL
url = os.environ['REST_URL']

# # headers
headers = os.environ['API_HEADER']

# sample data
temp = {
    "color": "black",
    "size": 200
}

data = json.dumps(temp).encode('utf8')
req =  request.Request(url, data=data, headers=headers)
resp = request.urlopen(req)
print(resp.read().decode('utf8'))
