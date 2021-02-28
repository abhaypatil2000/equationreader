import os
from gtts import gTTS
from gtts import lang

input_file = "./Files/out2.txt"
output_file = "./Files/audio.mp3"

input_text = open(input_file, "r").read().replace("\n", " ")
language = "en"

output = gTTS(text=input_text, lang=language, slow=False)
input_file.close()
output.save(output_file)
