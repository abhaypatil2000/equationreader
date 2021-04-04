# the mathpix.py is the final production module
# this is for testing purpose

import os
import base64
import requests
import json
from pdf_to_image import *

output_file = "./test.txt"


def convert_pdf_to_latex(input_image):

    input_image = f'./{input_image}'

    image_uri = "data:image/png;base64," + base64.b64encode(
        open(input_image, "rb").read()).decode()
    r = requests.post("https://api.mathpix.com/v3/text",
                      data=json.dumps({'src': image_uri}),
                      headers={
                          "app_id": "2018csb1063_iitrpr_ac_in_3b2e55_7b249e",
                          "app_key": "06dcfdf863bb8d34f133",
                          "Content-type": "application/json"
                      })
    output = json.dumps(json.loads(r.text), indent=4, sort_keys=True)

    with open(output_file, 'w') as f:
        f.write(output)
        f.close()


# danger passed

convert_pdf_to_latex("./request1/images/page0.png", "request1")