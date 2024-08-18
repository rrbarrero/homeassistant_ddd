from domain.command_handlers.read_remote_state_command_handler import ReadRemoteStateCommandHandler
from domain.commands import Command, ReadRemoteStateCommand
from domain.dispatcher import InMemoryCommandDispatcher, InMemoryCommandDispatcherBuilder
from domain.events import RemoteStateReadedEvent
from domain.policy_handlers.remote_state_readed_policy_handler import RemoteStateReadedPolicyHandler
from domain.projection_handlers.debug_projection_handler import DebugProjectionHandler
from infra.ha_repository.in_memory import CURRENT_STATE_AA, InMemoryHaRepository


def test_remote_state_read():

    repo = InMemoryHaRepository()
    spy = []
    
    dispatcher: InMemoryCommandDispatcher = (
        InMemoryCommandDispatcherBuilder()
        .with_command_handler(
            command_type=ReadRemoteStateCommand,
            handler=ReadRemoteStateCommandHandler(repository=repo),
        )
        .with_policy_handler(
            event_type=RemoteStateReadedEvent,
            policy=RemoteStateReadedPolicyHandler(),
        )
        .with_projection_handler(
            event_type=RemoteStateReadedEvent,
            handler=DebugProjectionHandler(spy=spy),
        )
        .build()
    )

    commands: list[Command] = [ReadRemoteStateCommand(endpoint="/abc")]
    dispatcher.register(commands=commands)

    dispatcher.run()

    expected = RemoteStateReadedEvent(current_state=CURRENT_STATE_AA)
    assert dispatcher.events == [expected]
    assert spy == [expected]