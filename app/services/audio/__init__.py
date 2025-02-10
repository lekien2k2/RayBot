# -*- coding: utf-8 -*-
import subprocess
from .tts_model import text_to_speech


text = "Cảm ơn quý khách đã dùng bữa tại Trend Coffe. Hy vọng quý khách có trải nghiệm tuyệt vời!"
output_file = "./app/services/audio/sound_output.mp3"


# text_to_speech(text, "vi-VN-HoaiMyNeural", output_file)


# try:
#     subprocess.run(["ffplay", "-nodisp", "-autoexit", output_file], check=True)
# except subprocess.CalledProcessError:
#     print("Error when run mp3 file")


def speak(text):
    text_to_speech(text, "vi-VN-HoaiMyNeural", output_file)
    try:
        subprocess.run(["ffplay", "-nodisp", "-autoexit", output_file], check=True)
    except subprocess.CalledProcessError:
        print("Error when run mp3 file")
