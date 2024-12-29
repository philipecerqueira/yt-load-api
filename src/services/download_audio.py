from pytubefix import YouTube
from pytubefix.exceptions import VideoUnavailable

from src.utils.convert_to_mp3 import convert_to_mp3_service
from src.utils.file_manager import get_download_path


def download_audio_service(url: str) -> str:
    """
    Baixa o áudio de um vídeo do YouTube, converte para MP3 e retorna o caminho do arquivo.

    - **url**: URL do vídeo do YouTube
    - **Retorno**: Caminho do arquivo MP3 gerado

    - **Exceções**:
        - `ValueError`: Nenhum stream de áudio disponível.
        - `VideoUnavailable`: Vídeo não encontrado ou indisponível.
    """
    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()

        if not audio:
            raise ValueError("Nenhum stream de áudio disponível para este vídeo.")

        output = audio.download(output_path=get_download_path())
        mp3_path = convert_to_mp3_service(output)

        return mp3_path
    except VideoUnavailable as e:
        raise ValueError(f"Vídeo não encontrado ou indisponível: {url}") from e
