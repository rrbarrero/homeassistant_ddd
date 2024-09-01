from typing import Generic, Optional, TypeVar
from copy import copy
from domain.ddd import Aggregate, AggregateId


T = TypeVar("T", bound=Aggregate)


class ConcurrencyException(Exception):
    pass


class InMemoryAggregateRepository(Generic[T]):
    def __init__(self):
        self._storage: dict[str, T] = {}

    def save(self, aggregate: T) -> None:
        if aggregate.aggregate_id in self._storage:
            if aggregate.version != self._storage[aggregate.aggregate_id.value].version:
                raise ConcurrencyException("Concurrency exception")
        self._storage[aggregate.aggregate_id.value] = copy(aggregate)
        self._storage[aggregate.aggregate_id.value].version += 1

    def get(self, aggregate_id: AggregateId) -> Optional[T]:
        return self._storage.get(aggregate_id.value)
