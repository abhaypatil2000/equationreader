import sys
import os
import base64
import pdf2image
import requests
import json
from pdf_to_image import *


# folder_name can be the request ID generated
# pdf will be stored there, and so will be the latex files, extracted pages and audio file
def convert_pdf_to_latex(input_pdf, folder_name):
    # first convert all pages in pdf to images
    page_count = convert_pdf_to_images(input_pdf, folder_name)
    with os.scandir(f'{os.curdir}/{folder_name}/images') as it:
        for entry in sorted(it):
            if (entry.name.endswith(".png") and entry.is_file()):
                # put desired file path here
                input_image = f'./{folder_name}/{entry.name}'
                print(input_image)
                continue
                input_image = './pdftoimages/page0.png'
                output_file = input_image.replace("pdftoimages", "latex")
                image_uri = "data:image/png;base64," + base64.b64encode(
                    open(input_image, "rb").read()).decode()
                r = requests.post("https://api.mathpix.com/v3/text",
                                  data=json.dumps({'src': image_uri}),
                                  headers={
                                      "app_id":
                                      "2018csb1063_iitrpr_ac_in_3b2e55_7b249e",
                                      "app_key": "06dcfdf863bb8d34f133",
                                      "Content-type": "application/json"
                                  })
                output = json.dumps(json.loads(r.text),
                                    indent=4,
                                    sort_keys=True)

                with open(output_file, 'w') as f:
                    f.write("\n\n".join(output))


convert_pdf_to_latex("basic.pdf", "request1")