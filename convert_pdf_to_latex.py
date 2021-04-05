import sys
import os
import base64
import pdf2image
import requests
import json
from pdf_to_image import *
import glob


# folder_name can be the request ID generated
# pdf will be stored there and so will be extracted pages and audio file
# page count is the limit on pages to be processed
def convert_pdf_to_latex(input_pdf, folder_name, make_request, page_count):
    # first convert all pages in pdf to images
    # processed_pages is the actual number of pages processed
    processed_pages = convert_pdf_to_images(input_pdf, folder_name, page_count)
    content = ""

    with os.scandir(f'{os.curdir}/{folder_name}/images') as it:
        # TODO iterate in sorted order
        try:  # if folder already exists then exception occurs
            os.mkdir(f"./{folder_name}/tex")
        except:  # else remove all the content in the folder
            for file in glob.glob(f"./{folder_name}/tex/*"):
                os.remove(file)
        for entry in it:
            if (entry.name.endswith(".png") and entry.is_file()):
                # put desired file path here
                input_image = f'./{folder_name}/images/{entry.name}'

                output_file = f'./{folder_name}/tex/{entry.name}'
                output_file = output_file.replace("png", "tex")

                print(input_image)
                print(output_file)

                image_uri = "data:image/png;base64," + base64.b64encode(
                    open(input_image, "rb").read()).decode()

                # for unsuccessful requests
                page_id = entry.name.replace(".png", "")
                output = f" ,, {page_id} missing ,, "

                # DANGER !! mathpix ahead
                if make_request:
                    r = requests.post(
                        "https://api.mathpix.com/v3/text",
                        data=json.dumps({'src': image_uri}),
                        headers={
                            "app_id": "2018csb1063_iitrpr_ac_in_3b2e55_7b249e",
                            "app_key": "06dcfdf863bb8d34f133",
                            "Content-type": "application/json"
                        })
                    # TODO : SATHWIK CHECK THIS
                    # TODO : check for successful_request or not depending on the request.status or from the output of the return request
                    # TODO : if connection error then try to resend the request so that the user does not waste his money for connection error
                    # TODO : else whatever you decide
                    successful_request = True
                    if (successful_request):
                        output = json.dumps(json.loads(r.text),
                                            indent=4,
                                            sort_keys=True)
                # danger passed
                content += output + " "
    return (processed_pages, content)


# to avoid precious requests to mathpix
# make make_request to False
# convert_pdf_to_latex("basic.pdf", "request1", False)