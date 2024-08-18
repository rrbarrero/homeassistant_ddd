from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TypeAlias
from typing_extensions import Self

watios: TypeAlias = float
degrees: TypeAlias = float


class Aggregate:
    pass


TemperatureBoundaries = tuple[degrees, degrees]

@dataclass
class Device:
    entity_id: str
    state: bool
    temperature: degrees
    boundaries: TemperatureBoundaries
    consumption: watios
    last_change: datetime

    @classmethod
    def create(
        cls,
        entity_id: str,
        temperature: degrees,
        boundaries: TemperatureBoundaries,
        consumption: watios,
        state: Optional[bool] = False,
        last_change: Optional[datetime] = None,
    ) -> Self:
        return cls(
            entity_id,
            state or False,
            temperature,
            boundaries,
            consumption,
            last_change or datetime.now(),
        )


@dataclass
class CurrentState(Aggregate):
    exceedance: watios
    devices_state: list[Device]

    @classmethod
    def create(cls, exceedance: watios, devices_state: list[Device]) -> Self:
        return cls(exceedance, devices_state)


@dataclass
class DeviceChangedState(Aggregate):
    device: Device