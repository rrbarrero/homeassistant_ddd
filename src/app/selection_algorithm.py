from dataclasses import replace
from domain.aggregates import CurrentState, Device


class SelectionAlgorithm:
    def handle(self, current_state: CurrentState) -> Device | None:
        raise NotImplementedError()
    

class NaiveSelectionAlgorithm(SelectionAlgorithm):
    def handle(self, current_state: CurrentState) -> Device | None:
        for device in current_state.devices_state:
            if not device.state:
                if device.temperature not in range(*device.boundaries): # type: ignore
                    if current_state.exceedance > (device.consumption + 400):
                        return replace(device, state=True)
        return None