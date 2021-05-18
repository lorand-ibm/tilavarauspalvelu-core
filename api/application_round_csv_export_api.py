import csv
import datetime
import io

from django.http import FileResponse, HttpResponse
from icalendar import Calendar, Event
from rest_framework import mixins, renderers, serializers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from applications import views
from applications.models import ApplicationEvent, ApplicationRound
from opening_hours.hours import get_opening_hours
from reservations.models import Reservation


class ApplicationRoundCsvViewSet(ViewSet):
    queryset = ApplicationRound.objects.all()

    def retrieve(self, request, *args, **kwargs):
        response = HttpResponse(
            content_type="text/csv",
            #headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
        )

        export_application_round_data(response=response)
        return response


def export_application_round_data(response: HttpResponse):
    rounds = ApplicationRound.objects.all()
    writer = csv.writer(response, delimiter=";", )
    for round in rounds:
        row = ""
        for field in ApplicationRound._meta._get_fields():
            row += getattr(round, field.name) + ","
            writer.writerow(row)
    return response

def export_reservation_unit_data(application_round: ApplicationRound) -> str:

    for reservation_unit in application_round.reservation_units.all():
            hours = get_opening_hours(reservation_unit.uuid, start_date=application_round.reservation_period_begin, end_date=application_round.reservation_period_end)
            [reservation_unit.name, reservation_unit.id, reservation_unit