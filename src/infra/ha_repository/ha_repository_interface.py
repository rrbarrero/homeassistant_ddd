from abc import ABC, abstractmethod

from domain.aggregates import DeviceChangedState
from domain.events import RemoteStateReadedEvent


class HaRepository(ABC):

    @abstractmethod
    def read_remote_state(self, endpoint: str) -> RemoteStateReadedEvent:
        raise NotImplementedError
    
    @abstractmethod
    def change_device_state(self, device_state: DeviceChangedState):
        raise NotImplementedError