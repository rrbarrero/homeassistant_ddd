from domain.commands import PowerOffDeviceCommand, PowerOnDeviceCommand
from domain.ddd import PolicyHandler
from domain.entities import CurrentState, CurrentStateStatus
from domain.events import DevicesCheckedEvent


class DevicesCheckedPolicyHandler(PolicyHandler):
    def handle(
        self, event: DevicesCheckedEvent
    ) -> PowerOffDeviceCommand | PowerOnDeviceCommand | None:
        if event.device_changed:
            command = PowerOffDeviceCommand
            if event.device_changed.state:
                command = PowerOnDeviceCommand
            state: CurrentState = CurrentState.new(
                exceedance=event.current_state.exceedance,
                devices_state=event.current_state.devices_state,
                status=CurrentStateStatus.STATE_RECALCULATED,
            )
            return command(
                current_state=state,
                device_to_change=event.device_changed,
            )
        return None
