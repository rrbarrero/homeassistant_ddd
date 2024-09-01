from abc import ABC, abstractmethod

from domain.entities import Device
from domain.events import CurrentStateChangedEvent


class HaRepository(ABC):

    @abstractmethod
    def read_remote_state(self, endpoint: str) -> CurrentStateChangedEvent:
        raise NotImplementedError
    
    @abstractmethod
    def change_device_state(self, device_state: Device) -> None:
        raise NotImplementedError
    