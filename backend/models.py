from dataclasses import dataclass

from sqlalchemy import String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class PostEntity(Base):
    __tablename__ = "wordpress_posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    post_title: Mapped[str] = mapped_column(String(255), nullable=False)
    post_tag: Mapped[str] = mapped_column(String(100), nullable=False)
    post_content: Mapped[str] = mapped_column(Text, nullable=False)


@dataclass
class PostRecord:
    id: int | None
    username: str
    email: str
    post_title: str
    post_tag: str
    post_content: str
