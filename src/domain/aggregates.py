from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TypeAlias
from typing_extensions import Self

Watio: TypeAlias = float
Degree: TypeAlias = float


class Aggregate:
    pass


TemperatureBoundaries = tuple[Degree, Degree]

@dataclass(frozen=True)
class Device:
    entity_id: str
    state: bool
    temperature: Degree
    boundaries: TemperatureBoundaries
    consumption: Watio
    last_change: datetime

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Device):
            return False
        return self.entity_id == other.entity_id

    @classmethod
    def create(
        cls,
        entity_id: str,
        temperature: Degree,
        boundaries: TemperatureBoundaries,
        consumption: Watio,
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


@dataclass(frozen=True)
class CurrentState(Aggregate):
    exceedance: Watio
    devices_state: list[Device]

    @classmethod
    def create(cls, exceedance: Watio, devices_state: list[Device]) -> Self:
        return cls(exceedance, devices_state)