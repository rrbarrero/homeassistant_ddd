from abc import ABC, abstractmethod


class ProjectionHandler(ABC):
    @abstractmethod
    def handle(self, event) -> None:
        pass