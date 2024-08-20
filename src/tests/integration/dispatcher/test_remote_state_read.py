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
from domain.events import DevicesCheckedEvent, CurrentStateChangedEvent
from domain.policy_handlers.devices_checked_policy_handler import (
    DevicesCheckedPolicyHandler,
)
from domain.policy_handlers.remote_state_readed_policy_handler import (
    RemoteStateReadedPolicyHandler,
)
from domain.projection_handlers.debug_projection_handler import DebugProjectionHandler
from infra.ha_repository.in_memory import InMemoryHaRepository


def test_dispatcher():

    repo = InMemoryHaRepository()
    selection_algorithm = NaiveSelectionAlgorithm()

    spy = []

    dispatcher: InMemoryCommandDispatcher = (
        InMemoryCommandDispatcherBuilder()
        .with_command_handler(
            command_type=ReadRemoteStateCommand,
            handler=ReadRemoteStateCommandHandler(repository=repo),
        )
        .with_command_handler(
            command_type=CheckDevicesCommand,
            handler=CheckDevicesCommandHandler(selection_algorithm=selection_algorithm),
        )
        .with_command_handler(
            command_type=PowerOnDeviceCommand,
            handler=PowerOnDeviceCommandHanlder(ha_repository=repo),
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

    # 2nd event start 'aa' aa/cc device
    assert spy[1].device_changed.entity_id == "aa"
    assert spy[1].device_changed.state is True
    assert spy[1].device_changed.consumption == 700

    # 3rd event exceedance is updated with the new consumption
    assert spy[2].current_state.exceedance == 1300

    # 4th event 'cc' is powered on
    assert spy[3].device_changed.entity_id == "cc"
    assert spy[3].device_changed.state is True
    assert spy[3].device_changed.consumption == 600

    # 5th exceedance is updated with the new consumption
    assert spy[4].current_state.exceedance == 700

    # No more room for new devices because the marginal offset (hardcoded to 400)
    assert spy[5].device_changed is None
