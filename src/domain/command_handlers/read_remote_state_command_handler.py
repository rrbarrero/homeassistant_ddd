from domain.commands import ReadRemoteStateCommand
from domain.ddd import CommandHandler
from domain.events import CurrentStateChangedEvent
from infra.aggreate_repository.aggregation_repository import InMemoryAggregateRepository
from infra.ha_repository.ha_repository_interface import HaRepository


class ReadRemoteStateCommandHandler(CommandHandler):
    def __init__(
        self, ha_repository: HaRepository, aggregate_repo: InMemoryAggregateRepository
    ) -> None:
        self.ha_repository: HaRepository = ha_repository
        self.aggregate_repo: InMemoryAggregateRepository = aggregate_repo

    def handle(self, command: ReadRemoteStateCommand) -> CurrentStateChangedEvent:
        changed_state: CurrentStateChangedEvent = self.ha_repository.read_remote_state(
            endpoint=command.endpoint
        )
        self.aggregate_repo.save(aggregate=changed_state.current_state)
        return changed_state
