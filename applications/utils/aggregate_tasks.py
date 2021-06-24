from celery import shared_task
from django.conf import settings

from applications.models import ApplicationEvent

def run_task_aggregate_task(task, *args):
    if settings.CELERY_ENABLED:
        task.delay(*args)
    else task

@shared_task
def create_application_event_schedule_aggregate_data(event_id):
    print(f"Starting: {event_id}")

    event = ApplicationEvent.objects.get(pk=event_id)
    from applications.utils.aggregate_data import (
        ApplicationEventScheduleResultAggregateDataCreator,
    )

    ApplicationEventScheduleResultAggregateDataCreator(event).run()
    print(f"Request: {event.id}")
