from abc import ABC, abstractmethod

from models import PostRecord


class IPostCsvReader(ABC):
    @abstractmethod
    def read_rows(self, file_path: str) -> list[dict[str, str]]:
        raise NotImplementedError


class IPostRepository(ABC):
    @abstractmethod
    def ensure_schema(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def save_posts(self, posts: list[PostRecord]) -> int:
        raise NotImplementedError

    @abstractmethod
    def delete_all_posts(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def fetch_posts(self, limit: int = 50, offset: int = 0) -> list[PostRecord]:
        raise NotImplementedError

    @abstractmethod
    def count_posts(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def create_post(self, post: PostRecord) -> PostRecord:
        raise NotImplementedError

    @abstractmethod
    def get_post_by_id(self, post_id: int) -> PostRecord | None:
        raise NotImplementedError

    @abstractmethod
    def update_post(self, post_id: int, post: PostRecord) -> PostRecord | None:
        raise NotImplementedError

    @abstractmethod
    def delete_post(self, post_id: int) -> bool:
        raise NotImplementedError


class IImportService(ABC):
    @abstractmethod
    def import_from_csv(self, file_path: str, mode: str = "append") -> int:
        raise NotImplementedError

    @abstractmethod
    def list_posts(self, limit: int = 50, offset: int = 0) -> list[PostRecord]:
        raise NotImplementedError

    @abstractmethod
    def count_posts(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def add_post(self, post: PostRecord) -> PostRecord:
        raise NotImplementedError

    @abstractmethod
    def get_post(self, post_id: int) -> PostRecord | None:
        raise NotImplementedError

    @abstractmethod
    def update_post(self, post_id: int, post: PostRecord) -> PostRecord | None:
        raise NotImplementedError

    @abstractmethod
    def delete_post(self, post_id: int) -> bool:
        raise NotImplementedError
