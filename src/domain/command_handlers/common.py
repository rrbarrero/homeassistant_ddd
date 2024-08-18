from abc import ABC, abstractmethod

from domain.commands import Command
from domain.events import Event


class CommandHandler(ABC):
    @abstractmethod
    def handle(self, command: Command) -> Event:
        pass
