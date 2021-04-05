from convert_pdf_to_latex import *
from latex_parser import *
from text_to_audio import *


# input_pdf is the name of the pdf
# folder_name is the folder in which pdf resides
# folder_name can be the request ID generated
# pdf will be stored there and so will be extracted pages and audio file
# will generate audio.mp3 in the folder_name folder
def convert_pdf_to_audio(input_pdf, folder_name, page_limit):
    # convert pdf to latex
    make_request = False  # make this true for testing #! TODO
    content = ""

    # this page_count will return actually how many pages are processed
    (processed_pages, content) = convert_pdf_to_latex(input_pdf, folder_name,
                                                      make_request, page_limit)

    # convert latext to intermediate text
    parsed_content = latex_parser(content)

    # use interpretter
    # generate audio.mp3 file
    text_to_audio(parsed_content, folder_name)

    return processed_pages
