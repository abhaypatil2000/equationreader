import os
import base64
import requests
import json
from pdf_to_image import *

# filelist = glob.glob(os.path.join(path, 'FV/*.txt'))
# for infile in sorted(filelist):
#     #do some fancy stuff
#     print str(infile)


# folder_name can be the request ID generated
# pdf will be stored there and so will be extracted pages and audio file
# page count is the limit on pages to be processed
def convert_pdf_to_latex(input_pdf, folder_name, make_request, page_count):
    # first convert all pages in pdf to images
    # processed_pages is the actual number of pages processed
    processed_pages = convert_pdf_to_images(input_pdf, folder_name, page_count)
    content = ""  # to be given further to latex_parser
    directory = f"./{folder_name}/images"
    for entry in sorted(os.listdir(directory)):
        # try:  # if folder already exists then exception occurs
        #     os.mkdir(f"./{folder_name}/tex")
        # except:  # else remove all the content in the folder
        #     for file in glob.glob(f"./{folder_name}/tex/*"):
        #         os.remove(file)
        if (entry.endswith(".png")):
            # put desired file path here
            input_image = f'./{folder_name}/images/{entry}'

            # output_file = f'./{folder_name}/tex/{entry.name}'
            # output_file = output_file.replace("png", "tex")

            print(input_image)

            image_uri = "data:image/png;base64," + base64.b64encode(
                open(input_image, "rb").read()).decode()

            # for unsuccessful requests
            page_id = entry.replace(".png", "")
            output = f" ,, {page_id} missing ,, "
            output = "\\( \\frac{1}{2}(x-3)+x=17+3(4-x) \\) ,, "  #! for testing
            print(f"{page_id} done")

            # DANGER !! mathpix ahead
            if make_request:
                r = requests.post("https://api.mathpix.com/v3/text",
                                  data=json.dumps({'src': image_uri}),
                                  headers={
                                      "app_id":
                                      "2018csb1063_iitrpr_ac_in_3b2e55_7b249e",
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
                    output = json.loads(output)["text"]
            # danger passed
            print(f"{page_id} done API request")
            content += output + " "
    return (processed_pages, content)


# to avoid precious requests to mathpix
# make make_request to False
# convert_pdf_to_latex("basic.pdf", "request1", False, some integer(upper bound for the number of pages to convert))