import pdftotext
# Load your PDF
with open("./Files/basic.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)
# Save all text to a txt file.
with open('./Files/temp.txt', 'w') as f:
    f.write("\n\n".join(pdf))

# import pdftotext

# f = open("./Files/basic.pdf", "r")
# pdf = pdftotext.PDF(f)

# output_file = open("./Files/temp.txt", "w")
# print()