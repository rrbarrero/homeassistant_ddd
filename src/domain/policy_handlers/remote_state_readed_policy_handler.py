from domain.commands import CheckDevicesCommand
from domain.events import RemoteStateReadedEvent
from domain.policy_handlers.common import PolicyHandler


class RemoteStateReadedPolicyHandler(PolicyHandler):
    def handle(self, event: RemoteStateReadedEvent) -> CheckDevicesCommand:
        return CheckDevicesCommand(current_state=event.current_state)