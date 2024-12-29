from pytubefix import YouTube
from pytubefix.exceptions import VideoUnavailable

from src.utils.file_manager import get_download_path


def download_video_service(url: str) -> str:
    """
    Baixa o vídeo do YouTube e retorna o caminho do arquivo.

    - **url**: URL do vídeo do YouTube
    - **Retorno**: Caminho do arquivo MP4 gerado

    - **Exceções**:
        - `ValueError`: Nenhum stream de vídeo disponível.
        - `VideoUnavailable`: Vídeo não encontrado ou indisponível.
    """
    try:
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension="mp4").first()

        if not video:
            raise ValueError("Nenhum stream de vídeo disponível para este vídeo.")

        output = video.download(output_path=get_download_path())
        return output
    except VideoUnavailable as e:
        raise ValueError(f"Vídeo não encontrado ou indisponível: {url}") from e
