from dataclasses import dataclass

from domain.aggregates import CurrentState, Device


class Event:
    pass


@dataclass
class RemoteStateReadedEvent(Event):
    current_state : CurrentState


@dataclass
class DevicesCheckedEvent(Event):
    current_state : CurrentState
    device_changed: Device | None