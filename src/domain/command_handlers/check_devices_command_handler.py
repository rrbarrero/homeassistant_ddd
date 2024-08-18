from app.selection_algorithm import SelectionAlgorithm
from domain.aggregates import DeviceChangedState
from domain.command_handlers.common import CommandHandler
from domain.commands import CheckDevicesCommand
from domain.events import DevicesCheckedEvent


class CheckDevicesCommandHandler(CommandHandler):

    def __init__(self, selection_algorithm: SelectionAlgorithm):
        self.selection_algorithm: SelectionAlgorithm = selection_algorithm

    def handle(self, command: CheckDevicesCommand) -> DevicesCheckedEvent:
        device_to_change: DeviceChangedState | None = self.selection_algorithm.handle(
            current_state=command.current_state
        )
        if device_to_change:
            return DevicesCheckedEvent(
                device_changed=device_to_change.device,
                current_state=command.current_state,
            )
        return DevicesCheckedEvent(
            device_changed=None, current_state=command.current_state
        )
