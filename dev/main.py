import os
import json
import requests

# URL
# url = 'http://'+os.environ['REST_URL'] + ':30000'
url = 'http://192.168.65.3:30000'
# headers
headers = {
    "Content-Type": "application/json"
}

# data
temp = {
    "color": "black",
    "size": 200
}

data = json.dumps(temp)

response = requests.post(url, headers=headers, data=data)

print("response: ", response)
print("response.text: ", response.text)