from dataclasses import dataclass

from domain.aggregates import CurrentState


class Command:
    pass


@dataclass
class ReadRemoteStateCommand(Command):
    endpoint: str

@dataclass
class CheckDevicesCommand(Command):
    current_state: CurrentState