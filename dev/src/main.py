import os
import json
from urllib import request

# # URL
url = os.environ['REST_URL']

# sample data
temp = { 
    "team_id": "convai",
    "secret": "3dlZhXRPPyt22tR9", 
    "answer_sheet": {
        "no": "1", 
        "answer": "20"
    }
}

# post to API server
data = json.dumps(temp).encode('utf8')
req =  request.Request(url, data=data)

# check API server return
resp = request.urlopen(req)
print(resp.read().decode('utf8'))