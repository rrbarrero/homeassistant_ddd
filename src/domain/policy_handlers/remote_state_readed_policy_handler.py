from domain.events import RemoteStateReadedEvent
from domain.policy_handlers.common import PolicyHandler


class RemoteStateReadedPolicyHandler(PolicyHandler):
    def handle(self, event: RemoteStateReadedEvent):
        print(f"TODO: Check devices command! with {event}")