# this is for testing an individual text file,
# not used to any production related work

import os
import base64
import requests
import json

folder_name = 'Report/hem4'
entry = 'inp.png'
f = open(f"./{folder_name}/mathpix.txt", "w")

input_image = f'./{folder_name}/{entry}'

print(input_image)

image_uri = "data:image/png;base64," + base64.b64encode(
    open(input_image, "rb").read()).decode()

r = requests.post("https://api.mathpix.com/v3/text",
                  data=json.dumps({'src': image_uri}),
                  headers={
                      "app_id": "2018csb1063_iitrpr_ac_in_3b2e55_7b249e",
                      "app_key": "06dcfdf863bb8d34f133",
                      "Content-type": "application/json"
                  })
print(r.status_code)
print(r.text)

output = json.dumps(json.loads(r.text), indent=4, sort_keys=True)
output = json.loads(output)["text"]

print(output)
f.write(output)