from dataclasses import dataclass

from domain.ddd import Command
from domain.entities import CurrentState, Device


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
