from domain.commands import CheckDevicesCommand
from domain.events import CurrentStateChangedEvent
from domain.policy_handlers.common import PolicyHandler


class RemoteStateReadedPolicyHandler(PolicyHandler):
    def handle(self, event: CurrentStateChangedEvent) -> CheckDevicesCommand:
        return CheckDevicesCommand(current_state=event.current_state)