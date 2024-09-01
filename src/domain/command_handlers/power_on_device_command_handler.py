from domain.entities import CurrentState, CurrentStateStatus, Device
from domain.commands import PowerOnDeviceCommand
from domain.ddd import CommandHandler
from domain.events import CurrentStateChangedEvent
from infra.aggreate_repository.aggregation_repository import InMemoryAggregateRepository
from infra.ha_repository.ha_repository_interface import HaRepository


class PowerOnDeviceCommandHanlder(CommandHandler):
    def __init__(
        self, ha_repository: HaRepository, aggregate_repo: InMemoryAggregateRepository
    ) -> None:
        self.ha_repo: HaRepository = ha_repository
        self.aggregate_repo: InMemoryAggregateRepository = aggregate_repo

    def handle(self, command: PowerOnDeviceCommand) -> CurrentStateChangedEvent:
        self.ha_repo.change_device_state(device_state=command.device_to_change)
        new_state: CurrentState = CurrentState.new(
            exceedance=self._update_exceedance(command=command),
            devices_state=self._update_devices_state(command=command),
            status=CurrentStateStatus.STATE_RECALCULATED,
        )
        self.aggregate_repo.save(aggregate=new_state)

        return CurrentStateChangedEvent(current_state=new_state)

    def _update_devices_state(self, command: PowerOnDeviceCommand) -> list[Device]:
        return [
            device if device != command.device_to_change else command.device_to_change
            for device in command.current_state.devices_state
        ]

    def _update_exceedance(self, command: PowerOnDeviceCommand) -> float:
        exceedance_delta: float = (
            -command.device_to_change.consumption
            if command.device_to_change.state
            else command.current_state.exceedance
        )

        return command.current_state.exceedance + exceedance_delta
