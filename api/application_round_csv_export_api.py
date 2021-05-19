import csv
import datetime

from django.http import HttpResponse
from rest_framework import mixins, viewsets

from applications.models import (
    Application,
    ApplicationEventSchedule,
    ApplicationRound,
    EventReservationUnit,
)
from opening_hours.hours import get_opening_hours
from tilavarauspalvelu.utils.date_util import next_or_current_matching_weekday

application_headers = [
    "application status",
    "applicant type",
    "applicant name",
    "organisation",
    "home city",
]

event_headers = [
    "event name",
    "events per week",
    "age group",
    "min duration",
    "max duration",
]

unit_headers = [
    "Mo",
    "Tu",
    "We",
    "Th",
    "Fr",
    "Sa",
    "Su",
    "Reservation unit name",
    "Unit id",
    "Priority",
]

schedule_headers = ["day", "Schedule begin", "Schedule end"]

header = application_headers + event_headers + unit_headers + schedule_headers


class ApplicationRoundCsvViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    queryset = ApplicationRound.objects.all()

    def list(self, request, *args, **kwargs):
        response = HttpResponse(
            content_type="text/csv",
        )
        for application_round in ApplicationRound.objects.all():

            export_application_round_data(response, application_round)
        return response

    def retrieve(self, request, *args, **kwargs):
        response = HttpResponse(
            content_type="text/csv",
        )

        export_application_round_data(
            response=response,
            application_round=ApplicationRound.objects.get(pk=kwargs["pk"]),
        )
        return response


def export_application_round_data(
    response: HttpResponse, application_round: ApplicationRound
):
    writer = csv.writer(
        response,
        delimiter=";",
    )
    writer.writerow(header)
    for application in application_round.applications.filter():

        for event_data in export_event_data(
            application=application, application_round=application_round
        ):
            application_data = export_application_data(application)
            writer.writerow(application_data + event_data)

    return response


def export_application_data(application: Application):
    return [
        application.status,
        application.applicant_type,
        application.user.get_full_name(),
        application.organization.name if hasattr(application, "organization") else "-",
        application.home_city.name if application.home_city is not None else "",
    ]


def export_event_data(application: Application, application_round: ApplicationRound):
    event_data = []
    for application_event in application.application_events.all():

        for space in application_event.event_reservation_units.all():
            unit_data = export_single_reservation_unit(space, application_round)
            for schedule in application_event.application_event_schedules.all():
                data = [
                    application_event.name,
                    application_event.events_per_week,
                    f"{application_event.age_group.minimum}-{application_event.age_group.maximum}",
                    application_event.min_duration,
                    application_event.max_duration
                    if application_event.max_duration is not None
                    else application_event.min_duration,
                ]
                data += unit_data + export_schedule_data(schedule)
                event_data.append(data)

    return event_data


def export_schedule_data(schedule: ApplicationEventSchedule):
    switcher = {0: "Mo", 1: "Tu", 2: "We", 3: "Th", 4: "Fr", 5: "Sa", 6: "Su"}
    data = [switcher[schedule.day], schedule.begin, schedule.end]
    return data


def export_single_reservation_unit(
    event_reservation_unit: EventReservationUnit, application_round: ApplicationRound
):
    row_values = []
    hours = get_opening_hours(
        event_reservation_unit.reservation_unit.uuid,
        start_date=application_round.reservation_period_begin,
        end_date=application_round.reservation_period_end,
    )
    monday = next_or_current_matching_weekday(
        application_round.reservation_period_begin, 0
    )
    for i in range(0, 7):
        wk = monday + datetime.timedelta(days=i)

        hour = next((obj for obj in hours if obj["date"] == wk), None)
        if hour and len(hour["times"]) > 0:
            row_values.append(
                f"{hour['times'][0].start_time}-{hour['times'][0].end_time}"
            )
        else:
            row_values.append("-")

    row_values += [
        event_reservation_unit.reservation_unit.name,
        str(event_reservation_unit.reservation_unit.id),
        event_reservation_unit.priority,
    ]
    return row_values
