from fastapi import FastAPI

from src.routers import download

app = FastAPI(title="YT Load", description="API simples e prática de download")

app.include_router(download.router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "API de download em execução"}
