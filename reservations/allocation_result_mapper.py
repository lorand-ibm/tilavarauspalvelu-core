from reservations.allocation_solver import AllocatedEvent


class AllocationResultMapper(object):

    def __init__(self, allocated_events: [AllocatedEvent]):
        self.allocated_events = allocated_events

