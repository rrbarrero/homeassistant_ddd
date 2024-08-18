import datetime
from app.selection_algorithm import NaiveSelectionAlgorithm
from domain.aggregates import Device
from domain.command_handlers.check_devices_command_handler import (
    CheckDevicesCommandHandler,
)
from domain.command_handlers.read_remote_state_command_handler import (
    ReadRemoteStateCommandHandler,
)
from domain.commands import CheckDevicesCommand, Command, ReadRemoteStateCommand
from domain.dispatcher import (
    InMemoryCommandDispatcher,
    InMemoryCommandDispatcherBuilder,
)
from domain.events import DevicesCheckedEvent, RemoteStateReadedEvent
from domain.policy_handlers.devices_checked_policy_handler import (
    DevicesCheckedPolicyHandler,
)
from domain.policy_handlers.remote_state_readed_policy_handler import (
    RemoteStateReadedPolicyHandler,
)
from domain.projection_handlers.debug_projection_handler import DebugProjectionHandler
from infra.ha_repository.in_memory import CURRENT_STATE_AA, InMemoryHaRepository


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
        .with_policy_handler(
            event_type=RemoteStateReadedEvent,
            policy=RemoteStateReadedPolicyHandler(),
        )
        .with_policy_handler(
            event_type=DevicesCheckedEvent,
            policy=DevicesCheckedPolicyHandler(),
        )
        .with_projection_handler(
            event_type=RemoteStateReadedEvent,
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

    event1 = RemoteStateReadedEvent(current_state=CURRENT_STATE_AA)
    event2 = DevicesCheckedEvent(
        current_state=CURRENT_STATE_AA,
        device_changed=Device(
            entity_id="aa",
            state=True,
            temperature=27,
            boundaries=(18, 26),
            consumption=300,
            last_change=datetime.datetime(2024, 1, 1, 0, 0),
        ),
    )
    
    assert spy == [event1, event2]
