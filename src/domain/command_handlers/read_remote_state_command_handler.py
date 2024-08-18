from domain.command_handlers.common import CommandHandler
from domain.commands import ReadRemoteStateCommand
from domain.events import RemoteStateReadedEvent
from infra.ha_repository.ha_repository_interface import HaRepository


class ReadRemoteStateCommandHandler(CommandHandler):
    def __init__(self, repository: HaRepository) -> None:
        self.repo: HaRepository = repository

    def handle(self, command: ReadRemoteStateCommand) -> RemoteStateReadedEvent:
        return self.repo.read_remote_state(endpoint=command.endpoint)
