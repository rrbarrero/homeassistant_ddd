from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, TypeAlias
from typing_extensions import Self

from domain.ddd import Aggregate, AggregateId


Watio: TypeAlias = float
Degree: TypeAlias = float


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


class CurrentStateId(AggregateId):
    pass


class CurrentStateStatus(Enum):
    POWER_ON = "POWER_ON"
    POWER_OFF = "POWER_OFF"
    DEVICE_CHECK = "DEVICE_CHECK"
    REMOTE_READED = "REMOTE_READED"


class CurrentState(Aggregate):

    def __init__(
        self,
        id: CurrentStateId,
        version: int,
        exceedance: Watio,
        devices_state: list[Device],
        status: CurrentStateStatus,
    ) -> None:
        super().__init__(aggregate_id=id, version=version)

        self.exceedance = exceedance
        self.devices_state: list[Device] = devices_state
        self.status = status

    @classmethod
    def new(
        cls, exceedance: Watio, devices_state: list[Device], status: CurrentStateStatus
    ) -> Self:
        return cls(
            id=CurrentStateId.new(),
            version=0,
            exceedance=exceedance,
            devices_state=devices_state,
            status=status,
        )

    @classmethod
    def update_device_state(cls, current_state: Self, device_to_change: Optional[Device]) -> Self:
        if device_to_change is None:
            return current_state
        devices_update = [
            device
            if device.entity_id != device_to_change.entity_id
            else device_to_change
            for device in current_state.devices_state
        ]
        return cls(
            id=current_state.aggregate_id, # type: ignore
            version=current_state.version,
            exceedance=current_state.exceedance,
            devices_state=devices_update,
            status=CurrentStateStatus.DEVICE_CHECK,
        )
