from domain.aggregates import CurrentState
from domain.command_handlers.common import CommandHandler
from domain.commands import PowerOnDeviceCommand
from domain.events import CurrentStateChangedEvent
from infra.ha_repository.ha_repository_interface import HaRepository


class PowerOnDeviceCommandHanlder(CommandHandler):
    def __init__(self, ha_repository: HaRepository) -> None:
        self.repo: HaRepository = ha_repository

    def handle(self, command: PowerOnDeviceCommand) -> CurrentStateChangedEvent:
        self.repo.change_device_state(device_state=command.device_to_change)
        devices_updated = []
        for device in command.current_state.devices_state:
            if device.entity_id == command.device_to_change.entity_id:
                devices_updated.append(command.device_to_change)
            else:
                devices_updated.append(device)
        updated_exceedance: float = (
            command.current_state.exceedance - command.device_to_change.consumption
        )
        if not command.device_to_change.state:
            updated_exceedance = (
                command.current_state.exceedance + command.current_state.exceedance
            )
        return CurrentStateChangedEvent(
            current_state=CurrentState.create(
                exceedance=updated_exceedance, devices_state=devices_updated
            ),
        )
