import os

input_file = "./Files/out1.txt"
output_file = "./Files/out2.txt"

input_text = open(input_file, "r").read()
# print(input_text)

output_text = input_text
output_text = output_text.replace("√", " square root ")
output_text = output_text.replace("^", " raised to ")
output_text = output_text.replace("(", " open bracket ")
output_text = output_text.replace(")", " close bracket ")
output_text = output_text.replace("-", " minus ")
output_text = output_text.replace("+", " plus ")
output_text = output_text.replace("/", " divided by ")
output_text = output_text.replace("\n", " . next line. \n ")

while ("  " in output_text):
    output_text = output_text.replace("  ", " ")

f = open(output_file, "w")
f.write(output_text)
