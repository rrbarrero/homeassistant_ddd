from abc import ABC, abstractmethod
from typing_extensions import Self
from dataclasses import dataclass

from uuid import uuid4


@dataclass(frozen=True)
class AggregateId:
    value: str

    @classmethod
    def new(cls) -> Self:
        return cls(str(uuid4()))


class Aggregate:

    def __init__(self, aggregate_id: AggregateId, version: int) -> None:
        self.aggregate_id = aggregate_id
        self.version = version

    @classmethod
    @abstractmethod
    def from_dict(cls, aggregate_id: AggregateId, version: int, data: dict) -> Self:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class Command:
    pass


class Event:
    pass


class CommandHandler(ABC):
    @abstractmethod
    def handle(self, command: Command) -> Event:
        pass


class ProjectionHandler(ABC):
    @abstractmethod
    def handle(self, event) -> None:
        pass


class PolicyHandler(ABC):
    @abstractmethod
    def handle(self, event) -> Command | None:
        pass
