# import pdftotext

# with open("./Report/hem4/hemh101-4.pdf", "rb") as f:
#     pdf = pdftotext.PDF(f)

# with open('./Report/hem4/pdftotext.txt', 'w') as f:
#     f.write("\n\n".join(pdf))

from src.pdf_to_image import convert_pdf_to_images

convert_pdf_to_images("inp.pdf", "Report/hem1", 1)