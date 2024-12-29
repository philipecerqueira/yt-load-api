import os
import time
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.services.download_audio import download_audio_service
from src.utils.logger_config import get_logger
from src.utils.remove_file import remove_file

logger = get_logger(__name__)
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
    start_time = time.perf_counter()
    logger.info(
        f"Requisição recebida: /download/audio, params: url={url}, filename={filename}"
    )

    try:
        mp3_file = download_audio_service(url, filename)
        logger.info(f"Áudio baixado com sucesso: {mp3_file}")

        background_tasks.add_task(remove_file, mp3_file)
        logger.info(f"Tarefa de remoção agendada para o arquivo: {mp3_file}")

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        logger.info(f"Requisição finalizada. Tempo total: {elapsed_time:.2f} segundos")

        return FileResponse(
            mp3_file, media_type="audio/mpeg", filename=os.path.basename(mp3_file)
        )
    except Exception as e:
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        logger.error(
            f"Erro ao processar a requisição: {e}. Tempo total: {elapsed_time:.2f} segundos",
            exc_info=True,
        )

        raise HTTPException(
            status_code=500,
            detail="Erro ao baixar arquivo, tente novamente mais tarde.",
        )
