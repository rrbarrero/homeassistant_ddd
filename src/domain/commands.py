from dataclasses import dataclass


class Command:
    pass


@dataclass
class ReadRemoteStateCommand(Command):
    endpoint: str