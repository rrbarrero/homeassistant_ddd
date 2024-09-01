import datetime
from domain.entities import CurrentState, CurrentStateStatus, Device
from domain.events import CurrentStateChangedEvent
from infra.ha_repository.ha_repository_interface import HaRepository

DATE_AA = datetime.datetime(year=2024, month=1, day=1, hour=0, minute=0, second=0)

DEVICE_AA: Device = Device.create(
    entity_id="aa",
    temperature=27,
    boundaries=(18, 26),
    consumption=700,
    state=False,
    last_change=DATE_AA,
)
DEVICE_BB: Device = Device.create(
    entity_id="bb",
    temperature=22,
    boundaries=(19, 27),
    consumption=600,
    state=False,
    last_change=DATE_AA,
)
DEVICE_CC: Device = Device.create(
    entity_id="cc",
    temperature=28,
    boundaries=(19, 27),
    consumption=600,
    state=False,
    last_change=DATE_AA,
)
DEVICE_DD: Device = Device.create(
    entity_id="dd",
    temperature=28,
    boundaries=(19, 27),
    consumption=600,
    state=False,
    last_change=DATE_AA,
)

CURRENT_STATE_AA: CurrentState = CurrentState.new(
    exceedance=2000,
    devices_state=[DEVICE_AA, DEVICE_BB, DEVICE_CC, DEVICE_DD],
    status=CurrentStateStatus.REMOTE_READED,
)


class InMemoryHaRepository(HaRepository):
    def __init__(self) -> None:
        self._params = None

    def read_remote_state(self, endpoint: str) -> CurrentStateChangedEvent:
        self._params = endpoint
        return CurrentStateChangedEvent(current_state=CURRENT_STATE_AA)

    def change_device_state(self, device_state: Device) -> None:
        self._params = device_state
