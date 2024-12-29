import os
import time
from enum import Enum
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.services.download_audio import download_audio_service
from src.services.download_video import download_video_service
from src.utils.logger_config import get_logger
from src.utils.remove_file import remove_file

logger = get_logger(__name__)
router = APIRouter()


class FileType(str, Enum):
    mp3 = "mp3"
    mp4 = "mp4"


class DownloadRequest(BaseModel):
    url: str
    file_type: Optional[FileType] = FileType.mp3


@router.get("/download")
async def download(
    background_tasks: BackgroundTasks,
    url: str,
    file_type: Optional[FileType] = FileType.mp3,
) -> FileResponse:
    """
    Baixa um arquivo (áudio ou vídeo) do YouTube e retorna o arquivo para download.

    - **url**: URL do vídeo do YouTube
    - **file_type**: Tipo de arquivo, pode ser 'mp3' para áudio ou 'mp4' para vídeo (padrão 'mp3')
    """
    start_time = time.perf_counter()
    logger.info(f"Requisição recebida, params: url={url}, file_type={file_type}")

    try:
        file_type_mapping = {
            FileType.mp3: {
                "service": download_audio_service,
                "media_type": "audio/mpeg",
                "extension": "mp3",
            },
            FileType.mp4: {
                "service": download_video_service,
                "media_type": "video/mp4",
                "extension": "mp4",
            },
        }

        file_info = file_type_mapping[file_type]

        file_path = file_info["service"](url)
        media_type = file_info["media_type"]
        file_extension = file_info["extension"]
        logger.info(
            f"Arquivo {file_extension.upper()} baixado com sucesso: {file_path}"
        )

        background_tasks.add_task(remove_file, file_path)
        logger.info(f"Tarefa de remoção agendada para o arquivo: {file_path}")

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        logger.info(f"Requisição finalizada. Tempo total: {elapsed_time:.2f} segundos")

        return FileResponse(
            file_path, media_type=media_type, filename=os.path.basename(file_path)
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
