import os

from pydub import AudioSegment


def convert_to_mp3_service(file_path: str) -> str:
    base_name, _ = os.path.splitext(file_path)
    new_mp3_path = f"{base_name}.mp3"
    AudioSegment.from_file(file_path).export(new_mp3_path, format="mp3")
    os.remove(file_path)

    return new_mp3_path
