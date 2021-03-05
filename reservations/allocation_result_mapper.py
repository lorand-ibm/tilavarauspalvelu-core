from applications.models import ApplicationEventResult, ApplicationEvent, ApplicationEventScheduleResult, \
    ApplicationEventSchedule
from reservations.allocation_models import integet_to_time_from_precision, ALLOCATION_PRECISION
from reservations.allocation_solver import AllocatedEvent


class AllocationResultMapper(object):

    def __init__(self, allocated_events: [AllocatedEvent]):
        self.allocated_events = allocated_events

    def to_events(self):
        for allocated_event in self.allocated_events:
            res
            try:
                res = ApplicationEventResult.objects.get(pk=allocated_event.event_id)
            except ApplicationEventResult.DoesNotExist:
                res = ApplicationEventResult.objects.create(application_event_ptr=ApplicationEvent.objects.get(pk=allocated_event.event_id))
            res.save()
            schedule
            try:
                schedule = ApplicationEventScheduleResult.objects.get(pk=allocated_event.occurrence_id)
            except ApplicationEventResult.DoesNotExist:
                schedule = ApplicationEventResult.objects.create(application_event_ptr=ApplicationEventSchedule.objects.get(pk=allocated_event.event_id), application_event_result=res)

            foo = schedule.application_event_ptr
            schedule.allocated_day = foo.day
            schedule.allocated_duration = allocated_event.duration
            schedule.allocated_begin = allocated_event.begin
            schedule.allocated_end = allocated_event.end
            schedule.save()




