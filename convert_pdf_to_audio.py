from convert_pdf_to_latex import *
from latex_parser import *
from text_to_audio import *


# input_pdf is the name of the pdf
# folder_name is the folder in which pdf resides
# will generate audio.mp3 in the folder_name folder
def convert_pdf_to_audio(input_pdf, folder_name):
    # convert pdf to latex
    make_request = False
    page_count = convert_pdf_to_latex(input_pdf, folder_name)

    # content from mathpix API
    content = ""

    # convert latext to intermediate text
    parsed_content = latex_parser(content)

    # use interpretter
    # generate audio file
    text_2_audio(parsed_content, folder_name)
