from abc import ABC, abstractmethod


class IImportPresenter(ABC):
    @abstractmethod
    def show_result(self, inserted_count: int) -> None:
        raise NotImplementedError
