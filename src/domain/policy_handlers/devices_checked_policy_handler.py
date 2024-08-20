from domain.commands import Command, PowerOffDeviceCommand, PowerOnDeviceCommand
from domain.events import DevicesCheckedEvent
from domain.policy_handlers.common import PolicyHandler


class DevicesCheckedPolicyHandler(PolicyHandler):
    def handle(self, event: DevicesCheckedEvent) -> Command | None:
        if event.device_changed:
            command = PowerOffDeviceCommand
            if event.device_changed.state:
                command = PowerOnDeviceCommand
            return command(
                current_state=event.current_state,
                device_to_change=event.device_changed,
            )
        return None
