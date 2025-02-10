import subprocess
import os


def text_to_speech(text, voice="vi-VN-HoaiMyNeural", output_file="sound_output.mp3"):
    temp_file = "./app/services/audio/tts_model/temp_text.txt"

    # Kiểm tra trước khi chạy
    print(
        f"Checking if output file exists before execution: {output_file} -> {os.path.exists(output_file)}"
    )

    if not os.path.exists(output_file):
        with open(output_file, "w") as f:
            pass

    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(text)

    command = [
        "python",
        "-m",
        "edge_tts",
        "--voice",
        voice,
        "--file",
        temp_file,
        "--write-media",
        output_file,
    ]

    try:
        subprocess.run(command, check=True)
        print("Done generating sound")
    except subprocess.CalledProcessError as e:
        print("Error generating sound")
        print(e)

    # Kiểm tra sau khi chạy
    print(
        f"Checking if output file exists after execution: {output_file} -> {os.path.exists(output_file)}"
    )
    if os.path.exists(output_file):
        print(f"Output file location: {os.path.abspath(output_file)}")
