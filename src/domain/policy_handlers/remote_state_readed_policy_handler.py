from domain.commands import CheckDevicesCommand
from domain.ddd import PolicyHandler
from domain.entities import CurrentState, CurrentStateStatus
from domain.events import CurrentStateChangedEvent


class RemoteStateReadedPolicyHandler(PolicyHandler):
    def handle(self, event: CurrentStateChangedEvent) -> CheckDevicesCommand:
        state: CurrentState = CurrentState.new(
            exceedance=event.current_state.exceedance,
            devices_state=event.current_state.devices_state,
            status=CurrentStateStatus.MANAGED_DEVICE,
        )
        return CheckDevicesCommand(current_state=state)
