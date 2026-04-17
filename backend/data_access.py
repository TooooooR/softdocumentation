import csv

from sqlalchemy import create_engine, delete, func, select
from sqlalchemy.orm import Session, sessionmaker

from interfaces import IPostCsvReader, IPostRepository
from models import Base, PostEntity, PostRecord


class CsvPostReader(IPostCsvReader):
    def read_rows(self, file_path: str) -> list[dict[str, str]]:
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]


class SqlAlchemyPostRepository(IPostRepository):
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, future=True)
        self._session_factory = sessionmaker(bind=self._engine, future=True)

    def ensure_schema(self) -> None:
        Base.metadata.create_all(self._engine)

    def save_posts(self, posts: list[PostRecord]) -> int:
        entities = [
            PostEntity(
                username=item.username,
                email=item.email,
                post_title=item.post_title,
                post_tag=item.post_tag,
                post_content=item.post_content,
            )
            for item in posts
        ]

        with Session(self._engine) as session:
            session.add_all(entities)
            session.commit()

        return len(entities)

    def delete_all_posts(self) -> int:
        with Session(self._engine) as session:
            result = session.execute(delete(PostEntity))
            session.commit()
            return int(result.rowcount or 0)

    def fetch_posts(self, limit: int = 50, offset: int = 0) -> list[PostRecord]:
        with Session(self._engine) as session:
            stmt = select(PostEntity).order_by(PostEntity.id).offset(offset).limit(limit)
            rows = session.execute(stmt).scalars().all()

        return [
            PostRecord(
                id=row.id,
                username=row.username,
                email=row.email,
                post_title=row.post_title,
                post_tag=row.post_tag,
                post_content=row.post_content,
            )
            for row in rows
        ]

    def count_posts(self) -> int:
        with Session(self._engine) as session:
            stmt = select(func.count(PostEntity.id))
            value = session.execute(stmt).scalar_one()
        return int(value)

    def create_post(self, post: PostRecord) -> PostRecord:
        entity = PostEntity(
            username=post.username,
            email=post.email,
            post_title=post.post_title,
            post_tag=post.post_tag,
            post_content=post.post_content,
        )

        with Session(self._engine) as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)

        return PostRecord(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            post_title=entity.post_title,
            post_tag=entity.post_tag,
            post_content=entity.post_content,
        )

    def get_post_by_id(self, post_id: int) -> PostRecord | None:
        with Session(self._engine) as session:
            entity = session.get(PostEntity, post_id)

        if entity is None:
            return None

        return PostRecord(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            post_title=entity.post_title,
            post_tag=entity.post_tag,
            post_content=entity.post_content,
        )

    def update_post(self, post_id: int, post: PostRecord) -> PostRecord | None:
        with Session(self._engine) as session:
            entity = session.get(PostEntity, post_id)
            if entity is None:
                return None

            entity.username = post.username
            entity.email = post.email
            entity.post_title = post.post_title
            entity.post_tag = post.post_tag
            entity.post_content = post.post_content
            session.commit()
            session.refresh(entity)

        return PostRecord(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            post_title=entity.post_title,
            post_tag=entity.post_tag,
            post_content=entity.post_content,
        )

    def delete_post(self, post_id: int) -> bool:
        with Session(self._engine) as session:
            entity = session.get(PostEntity, post_id)
            if entity is None:
                return False

            session.delete(entity)
            session.commit()

        return True
