from pytubefix import YouTube

from src.utils.convert_to_mp3 import convert_to_mp3_service
from src.utils.file_manager import get_download_path


def download_audio_service(url: str) -> str:
    yt = YouTube(url)
    audio = yt.streams.filter(only_audio=True).first()
    output = audio.download(output_path=get_download_path())
    mp3_path = convert_to_mp3_service(output)

    return mp3_path
