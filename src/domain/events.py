from dataclasses import dataclass

from domain.aggregates import CurrentState


class Event:
    pass


@dataclass
class RemoteStateReadedEvent(Event):
    current_state : CurrentState
