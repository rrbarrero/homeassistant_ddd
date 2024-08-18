from abc import ABC, abstractmethod

from domain.commands import Command


class PolicyHandler(ABC):
    @abstractmethod
    def handle(self, event) -> Command | None:
        pass