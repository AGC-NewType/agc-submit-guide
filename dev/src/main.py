import os
import json
import time
from urllib import request

# URL, template json load
url = os.environ['REST_ANSWER_URL']
template_path = '/home/agc2022/data/template.json'
with open(template_path,"r") as answer_json:
    json_data = json.load(answer_json)
    
    
# sample data
temp = {
        "no": "1", 
        "answer": "20"
    }
json_data['answer_sheet'].append(temp)
time.sleep(3)

# post to API server
data = json.dumps(temp).encode('unicode-escape')
req =  request.Request(url, data=data)

# check API server return
resp = request.urlopen(req)
status = resp.read().decode('utf8')
if "OK" in status:
    print("data requests successful!!")
    
# request end of mission message
message_structure = {
"team_id": "convai",
"secret": "3dlZhXRPPyt22tR9",
"end_of_mission": "true"
}

# json dump & encode unicode
tmp_message = json.dumps(message_structure).encode('unicode-escape')
request_message = request.Request(url, data=tmp_message) 
resp = request.urlopen(request_message) # POST