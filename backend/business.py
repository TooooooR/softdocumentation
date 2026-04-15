from interfaces import IImportService, IPostCsvReader, IPostRepository
from models import PostRecord


class ImportService(IImportService):
    def __init__(self, csv_reader: IPostCsvReader, repository: IPostRepository) -> None:
        self._csv_reader = csv_reader
        self._repository = repository

    def import_from_csv(self, file_path: str, mode: str = "append") -> int:
        rows = self._csv_reader.read_rows(file_path)
        posts: list[PostRecord] = []

        for row in rows:
            content = (row.get("post_content") or "").strip()
            words = content.split()
            limited_content = " ".join(words[:10])

            post = PostRecord(
                username=(row.get("username") or "").strip(),
                email=(row.get("email") or "").strip(),
                post_title=(row.get("post_title") or "").strip(),
                post_tag=(row.get("post_tag") or "").strip(),
                post_content=limited_content,
            )

            if all([post.username, post.email, post.post_title, post.post_tag, post.post_content]):
                posts.append(post)

        self._repository.ensure_schema()

        normalized_mode = mode.strip().lower()
        if normalized_mode not in {"append", "replace"}:
            raise ValueError("mode must be either 'append' or 'replace'")

        if normalized_mode == "replace":
            self._repository.delete_all_posts()

        return self._repository.save_posts(posts)

    def list_posts(self, limit: int = 50, offset: int = 0) -> list[PostRecord]:
        self._repository.ensure_schema()
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        return self._repository.fetch_posts(limit=safe_limit, offset=safe_offset)

    def count_posts(self) -> int:
        self._repository.ensure_schema()
        return self._repository.count_posts()
