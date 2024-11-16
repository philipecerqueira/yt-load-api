import os
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.services.download_audio import download_audio_service
from src.utils.remove_file import remove_file

router = APIRouter()


class DownloadRequest(BaseModel):
    url: str
    filename: Optional[str] = None


@router.get("/download/audio")
async def download_audio(
    background_tasks: BackgroundTasks, url: str, filename: Optional[str] = None
) -> FileResponse:
    """
    Baixa o áudio do YouTube e retorna um arquivo MP3 para download.

    - **url**: URL do vídeo do YouTube
    - **filename**: Nome opcional para o arquivo de áudio
    """
    try:
        mp3_file = download_audio_service(url, filename)

        background_tasks.add_task(remove_file, mp3_file)

        return FileResponse(
            mp3_file, media_type="audio/mpeg", filename=os.path.basename(mp3_file)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao baixar arquivo: {e}")
