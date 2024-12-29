from pytubefix import YouTube

from src.utils.file_manager import get_download_path


def download_video_service(url: str) -> str:
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True, file_extension="mp4").first()
    output = video.download(output_path=get_download_path())

    return output
