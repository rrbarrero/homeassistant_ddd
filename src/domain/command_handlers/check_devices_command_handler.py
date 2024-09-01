from app.selection_algorithm import SelectionAlgorithm
from domain.ddd import CommandHandler
from domain.entities import CurrentState, Device
from domain.commands import CheckDevicesCommand
from domain.events import DevicesCheckedEvent
from infra.aggreate_repository.aggregation_repository import InMemoryAggregateRepository


class CheckDevicesCommandHandler(CommandHandler):

    def __init__(
        self,
        selection_algorithm: SelectionAlgorithm,
        aggregate_repo: InMemoryAggregateRepository,
    ) -> None:
        self.selection_algorithm: SelectionAlgorithm = selection_algorithm
        self.aggregate_repo = aggregate_repo

    def handle(self, command: CheckDevicesCommand) -> DevicesCheckedEvent:
        device_to_change: Device | None = self.selection_algorithm.handle(
            current_state=command.current_state
        )
        devices_changed_event = DevicesCheckedEvent(
            device_changed=None, current_state=command.current_state
        )
        if device_to_change:
            devices_changed_event = DevicesCheckedEvent(
                device_changed=device_to_change,
                current_state=command.current_state,
            )
        self.aggregate_repo.save(
            aggregate=CurrentState.update_device_state(
                current_state=command.current_state, device_to_change=device_to_change
            )
        )
        return devices_changed_event
