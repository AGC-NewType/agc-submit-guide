from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

# for test env on docker
# url = os.environ['REST_URL']

# for test env on local
url  = '0.0.0.0'
error_test = False
@app.route("/test" ,methods=['POST'])
def test():
    # receive POST data
    params = request.get_data()
    received_params = json.loads(params.decode('utf-8'))
    print(received_params)
    # error occur if json has different keys
    if error_test:
        if len(list(received_params.keys())) != 3:
            response = {
                    "status": "ERROR",
                    "msg": "POST failed"
            }
        else:
            response = {
                    "status": "ok",
                    "msg": "POST success"
            }
    else:
        response = {
                        "status": "ok",
                        "msg": "POST success"
                }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, host=url)
