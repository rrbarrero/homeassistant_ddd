from abc import ABC, abstractmethod

from domain.events import RemoteStateReadedEvent


class HaRepository(ABC):

    @abstractmethod
    def read_remote_state(self, endpoint: str) -> RemoteStateReadedEvent:
        raise NotImplementedError