from dataclasses import dataclass

from domain.ddd import Event
from domain.entities import CurrentState, Device


@dataclass
class CurrentStateChangedEvent(Event):
    current_state: CurrentState


@dataclass
class DevicesCheckedEvent(Event):
    current_state: CurrentState
    device_changed: Device | None
