import os
import json
import time
from urllib import request

# REST URL load
url = os.environ['REST_ANSWER_URL']

# answer template
json_data = {
    "team_id": "userxx",
    "secret": "!@#$%^&*()",
    "answer_sheet": {}
}
    
    
# input sample data to template
temp = {
        "no": "1", 
        "answer": "20"
}
json_data['answer_sheet'] = temp

# post to API server
data = json.dumps(temp).encode('unicode-escape')
req =  request.Request(url, data=data)

# check API server return
resp = request.urlopen(req)
status = resp.read().decode('utf8')
if "OK" in status:
    print("data requests successful!!")
else if "ERROR" in status:
    raise ValueError("Receive ERROR status. Please check your source code.")    
    
# request end of mission message
message_structure = {
"team_id": "userxx",
"secret": "!@#$%^&*()",
"end_of_mission": "true"
}

# json dump & encode unicode
tmp_message = json.dumps(message_structure).encode('unicode-escape')
request_message = request.Request(url, data=tmp_message) 
resp = request.urlopen(request_message) # POST
