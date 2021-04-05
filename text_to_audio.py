from gtts import gTTS


def text_to_audio(parsed_content, folder_name):
    parsed_content = parsed_content.replace("(", " open bracket ")
    parsed_content = parsed_content.replace(")", " close bracket ")
    parsed_content = parsed_content.replace("-", " minus ")
    parsed_content = parsed_content.replace("+", " plus ")
    parsed_content = parsed_content.replace("/", " divided by ")
    parsed_content = parsed_content.replace("\n", " . next line. \n ")

    while ("  " in parsed_content):
        parsed_content = parsed_content.replace("  ", " ")

    tts = gTTS(parsed_content)
    tts.save(f'./{folder_name}/audio.mp3')