from dataclasses import dataclass

from domain.aggregates import CurrentState, Device


class Command:
    pass


@dataclass
class ReadRemoteStateCommand(Command):
    endpoint: str


@dataclass
class CheckDevicesCommand(Command):
    current_state: CurrentState


@dataclass
class PowerOnDeviceCommand(Command):
    current_state: CurrentState
    device_to_change: Device


@dataclass
class PowerOffDeviceCommand(Command):
    current_state: CurrentState
    device_to_change: Device
