from domain.ddd import ProjectionHandler
from domain.events import Event



class DebugProjectionHandler(ProjectionHandler):
    def __init__(self, spy: list) -> None:
        self.spy = spy
    
    def handle(self, event: Event) -> None:
        self.spy.append(event)