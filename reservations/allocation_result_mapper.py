from reservations.allocation_solver import AllocatedEvent


class AllocationResultMapper(object):

    def __init__(self, allocated_events: [AllocatedEvent]):
        self.allocated_events = allocated_events

    def to_events(self):
        for allocated_event in self.allocated_events:
            print("foo")

