from app.selection_algorithm import NaiveSelectionAlgorithm
from domain.command_handlers.check_devices_command_handler import (
    CheckDevicesCommandHandler,
)

from domain.command_handlers.power_on_device_command_handler import (
    PowerOnDeviceCommandHanlder,
)
from domain.command_handlers.read_remote_state_command_handler import (
    ReadRemoteStateCommandHandler,
)
from domain.commands import (
    CheckDevicesCommand,
    Command,
    PowerOnDeviceCommand,
    ReadRemoteStateCommand,
)
from domain.dispatcher import (
    InMemoryCommandDispatcher,
    InMemoryCommandDispatcherBuilder,
)
from domain.entities import CurrentState, CurrentStateStatus
from domain.events import DevicesCheckedEvent, CurrentStateChangedEvent
from domain.policy_handlers.devices_checked_policy_handler import (
    DevicesCheckedPolicyHandler,
)
from domain.policy_handlers.remote_state_readed_policy_handler import (
    RemoteStateReadedPolicyHandler,
)
from domain.projection_handlers.debug_projection_handler import DebugProjectionHandler
from infra.aggreate_repository.aggregation_repository import InMemoryAggregateRepository
from infra.ha_repository.in_memory import InMemoryHaRepository


def test_dispatcher():

    ha_repo = InMemoryHaRepository()
    aggregate_repo = InMemoryAggregateRepository()
    selection_algorithm = NaiveSelectionAlgorithm()

    spy = []

    dispatcher: InMemoryCommandDispatcher = (
        InMemoryCommandDispatcherBuilder()
        .with_command_handler(
            command_type=ReadRemoteStateCommand,
            handler=ReadRemoteStateCommandHandler(
                ha_repository=ha_repo, aggregate_repo=aggregate_repo
            ),
        )
        .with_command_handler(
            command_type=CheckDevicesCommand,
            handler=CheckDevicesCommandHandler(
                selection_algorithm=selection_algorithm, aggregate_repo=aggregate_repo
            ),
        )
        .with_command_handler(
            command_type=PowerOnDeviceCommand,
            handler=PowerOnDeviceCommandHanlder(
                ha_repository=ha_repo, aggregate_repo=aggregate_repo
            ),
        )
        .with_policy_handler(
            event_type=CurrentStateChangedEvent,
            policy=RemoteStateReadedPolicyHandler(),
        )
        .with_policy_handler(
            event_type=DevicesCheckedEvent,
            policy=DevicesCheckedPolicyHandler(),
        )
        .with_projection_handler(
            event_type=CurrentStateChangedEvent,
            handler=DebugProjectionHandler(spy=spy),
        )
        .with_projection_handler(
            event_type=DevicesCheckedEvent,
            handler=DebugProjectionHandler(spy=spy),
        )
        .build()
    )

    commands: list[Command] = [ReadRemoteStateCommand(endpoint="/abc")]
    dispatcher.register(commands=commands)

    dispatcher.run()

    # First read exceedance from HA
    assert spy[0].current_state.exceedance == 2000
    assert aggregation_state_at(spy=spy, aggregate_repo=aggregate_repo, index=0).status == CurrentStateStatus.REMOTE_READED

    # 2nd event start 'aa' aa/cc device
    assert spy[1].device_changed.entity_id == "aa"
    assert spy[1].device_changed.state is True
    assert spy[1].device_changed.consumption == 700
    assert aggregation_state_at(spy=spy, aggregate_repo=aggregate_repo, index=1).status == CurrentStateStatus.DEVICE_CHECK

    # 3rd event exceedance is updated with the new consumption
    assert spy[2].current_state.exceedance == 1300
    assert aggregation_state_at(spy=spy, aggregate_repo=aggregate_repo, index=2).status == CurrentStateStatus.POWER_ON

    # 4th event 'cc' is powered on
    assert spy[3].device_changed.entity_id == "cc"
    assert spy[3].device_changed.state is True
    assert spy[3].device_changed.consumption == 600
    assert aggregation_state_at(spy=spy, aggregate_repo=aggregate_repo, index=3).status == CurrentStateStatus.DEVICE_CHECK

    # 5th exceedance is updated with the new consumption
    assert spy[4].current_state.exceedance == 700
    assert aggregation_state_at(spy=spy, aggregate_repo=aggregate_repo, index=4).status == CurrentStateStatus.POWER_ON

    # No more room for new devices because the marginal offset (hardcoded to 400)
    assert spy[5].device_changed is None
    assert aggregation_state_at(spy=spy, aggregate_repo=aggregate_repo, index=5).status == CurrentStateStatus.DEVICE_CHECK

def aggregation_state_at(spy: list, aggregate_repo: InMemoryAggregateRepository, index: int) -> CurrentState:
    aggregate_id = spy[index].current_state.aggregate_id.value
    return aggregate_repo._storage[aggregate_id]