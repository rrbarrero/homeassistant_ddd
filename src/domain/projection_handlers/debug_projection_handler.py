from domain.events import Event
from domain.projection_handlers.common import ProjectionHandler


class DebugProjectionHandler(ProjectionHandler):
    def __init__(self, spy: list) -> None:
        self.spy = spy
    
    def handle(self, event: Event) -> None:
        self.spy.append(event)