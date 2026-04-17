from dataclasses import asdict
from typing import Literal

from fastapi import FastAPI

from di import build_import_service

DB_URL = "sqlite:///app.db"
service = build_import_service(db_url=DB_URL)

app = FastAPI(
    title="WordPress Import Backend",
    version="1.0.0",
    docs_url="/SWdocs",
    openapi_url="/openapi.json",
    redoc_url=None,
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Backend is running",
        "swagger": "/SWdocs",
        "get_posts": "/posts",
        "get_stats": "/stats",
    }


@app.get("/posts")
def get_posts(limit: int = 50, offset: int = 0) -> list[dict[str, str]]:
    posts = service.list_posts(limit=limit, offset=offset)
    return [asdict(post) for post in posts]


@app.get("/stats")
def get_stats() -> dict[str, int]:
    return {"total_posts": service.count_posts()}


@app.post("/import")
def import_posts(
    csv_path: str = "posts.csv",
    mode: Literal["append", "replace"] = "append",
) -> dict[str, int | str]:
    inserted = service.import_from_csv(file_path=csv_path, mode=mode)
    return {
        "inserted": inserted,
        "mode": mode,
        "total_after_import": service.count_posts(),
    }
