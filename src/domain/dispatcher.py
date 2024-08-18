from typing import Type
from typing_extensions import Self

from domain.command_handlers.common import CommandHandler
from domain.commands import Command
from domain.events import Event
from domain.policy_handlers.common import PolicyHandler
from domain.projection_handlers.common import ProjectionHandler


class InMemoryCommandDispatcher:
    def __init__(
        self,
        command_handlers: dict[Type[Command], CommandHandler],
        projection_handlers: dict[Type[Event], ProjectionHandler],
        policies: dict[Type[Event], list[PolicyHandler]],
    ) -> None:
        self.command_handlers: dict[type[Command], CommandHandler] = command_handlers
        self.projection_handlers: dict[type[Event], ProjectionHandler] = (
            projection_handlers
        )
        self.policies: dict[type[Event], list[PolicyHandler]] = policies

        self.commands: list[Command] = []
        self.events: list[Event] = []

    def register(self, commands: list[Command]) -> None:
        self.commands.extend(commands)

    def run(self) -> None:
        while self.commands:
            command: Command = self.commands.pop(0)
            handler: CommandHandler = self.command_handlers[type(command)]
            event: Event = handler.handle(command=command)
            if event:
                self.events.append(event)
            event_policies: list[PolicyHandler] = self.policies.get(type(event), [])
            for policy in event_policies:
                new_command: Command | None = policy.handle(event=event)
                if new_command:
                    self.commands.append(new_command)


        for event in self.events:
            event_handler: ProjectionHandler = self.projection_handlers[type(event)]
            event_handler.handle(event=event)


class InMemoryCommandDispatcherBuilder:
    def __init__(self):
        self.command_handlers: dict[Type[Command], CommandHandler] = {}
        self.projection_handlers: dict[Type[Event], ProjectionHandler] = {}
        self.policies: dict[Type[Event], list[PolicyHandler]] = {}

    def with_command_handler(
        self, command_type: Type[Command], handler: CommandHandler
    ) -> Self:
        self.command_handlers[command_type] = handler
        return self


    def with_policy_handler(self, event_type, policy) -> Self:
        if event_type not in self.policies:
            self.policies[event_type] = []

        self.policies[event_type].append(policy)
        return self

    def with_projection_handler(
        self, event_type: Type[Event], handler: ProjectionHandler
    ) -> Self:
        self.projection_handlers[event_type] = handler
        return self

    def build(self) -> InMemoryCommandDispatcher:
        return InMemoryCommandDispatcher(
            command_handlers=self.command_handlers,
            projection_handlers=self.projection_handlers,
            policies=self.policies,
        )
