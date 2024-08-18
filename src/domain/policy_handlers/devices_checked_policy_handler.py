from domain.commands import Command
from domain.events import DevicesCheckedEvent
from domain.policy_handlers.common import PolicyHandler


class DevicesCheckedPolicyHandler(PolicyHandler):
    def handle(self, event: DevicesCheckedEvent) -> Command | None:
        if event.device_changed:
            print("New command will be created")
            ### Here return the new command with the new overall state
            ### Remember to calculate the new exceedance
        return None