from dataclasses import asdict
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict

from di import build_import_service
from models import PostRecord

DB_URL = "sqlite:///app.db"
service = build_import_service(db_url=DB_URL)
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="WordPress Import Backend",
    version="1.0.0",
    docs_url="/SWdocs",
    openapi_url="/openapi.json",
    redoc_url=None,
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


class PostPayload(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    username: str
    email: str
    post_title: str
    post_tag: str
    post_content: str


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/posts")
def get_posts(limit: int = 100, offset: int = 0) -> list[dict[str, str | int | None]]:
    posts = service.list_posts(limit=limit, offset=offset)
    return [asdict(post) for post in posts]


@app.get("/posts/{post_id}")
def get_post(post_id: int) -> dict[str, str | int | None]:
    post = service.get_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return asdict(post)


@app.post("/posts")
def create_post(payload: PostPayload) -> dict[str, str | int | None]:
    try:
        created = service.add_post(
            PostRecord(
                id=None,
                username=payload.username,
                email=payload.email,
                post_title=payload.post_title,
                post_tag=payload.post_tag,
                post_content=payload.post_content,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return asdict(created)


@app.put("/posts/{post_id}")
def update_post(post_id: int, payload: PostPayload) -> dict[str, str | int | None]:
    try:
        updated = service.update_post(
            post_id,
            PostRecord(
                id=post_id,
                username=payload.username,
                email=payload.email,
                post_title=payload.post_title,
                post_tag=payload.post_tag,
                post_content=payload.post_content,
            ),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if updated is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return asdict(updated)


@app.delete("/posts/{post_id}")
def delete_post(post_id: int) -> dict[str, bool]:
    deleted = service.delete_post(post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"deleted": True}


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
