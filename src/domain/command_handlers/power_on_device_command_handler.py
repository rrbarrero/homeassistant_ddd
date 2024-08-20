from domain.aggregates import CurrentState, Device
from domain.command_handlers.common import CommandHandler
from domain.commands import PowerOnDeviceCommand
from domain.events import CurrentStateChangedEvent
from infra.ha_repository.ha_repository_interface import HaRepository


class PowerOnDeviceCommandHanlder(CommandHandler):
    def __init__(self, ha_repository: HaRepository) -> None:
        self.repo: HaRepository = ha_repository

    def handle(self, command: PowerOnDeviceCommand) -> CurrentStateChangedEvent:
        self.repo.change_device_state(device_state=command.device_to_change)

        return CurrentStateChangedEvent(
            current_state=CurrentState.create(
                exceedance=self._update_exceedance(command=command),
                devices_state=self._update_devices_state(command=command),
            ),
        )
    
    def _update_devices_state(self, command: PowerOnDeviceCommand) -> list[Device]:
        return [
            device if device != command.device_to_change else command.device_to_change
            for device in command.current_state.devices_state
        ]

    def _update_exceedance(self, command: PowerOnDeviceCommand) -> float:
        updated_exceedance: float = (
            command.current_state.exceedance - command.device_to_change.consumption
        )
        if not command.device_to_change.state:
            updated_exceedance = (
                command.current_state.exceedance + command.current_state.exceedance
            )
        return updated_exceedance