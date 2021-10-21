import datetime
import json
from unittest.mock import patch

import freezegun
import snapshottest
from assertpy import assert_that
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import get_default_timezone

from api.graphql.tests.base import GrapheneTestCaseBase
from applications.models import PRIORITY_CONST
from applications.tests.factories import ApplicationRoundFactory
from opening_hours.enums import State
from opening_hours.hours import TimeElement
from opening_hours.tests.test_get_periods import get_mocked_periods
from reservation_units.tests.factories import ReservationUnitFactory
from reservations.models import STATE_CHOICES, Reservation
from reservations.tests.factories import ReservationFactory
from spaces.tests.factories import SpaceFactory


@freezegun.freeze_time("2021-10-12T12:00:00Z")
class ReservationTestCaseBase(GrapheneTestCaseBase, snapshottest.TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.space = SpaceFactory()
        cls.reservation_unit = ReservationUnitFactory(pk=1, spaces=[cls.space])

    def get_mocked_opening_hours(self):
        resource_id = f"{settings.HAUKI_ORIGIN_ID}:{self.reservation_unit.uuid}"
        return [
            {
                "resource_id": resource_id,
                "origin_id": str(self.reservation_unit.uuid),
                "date": datetime.date.today(),
                "times": [
                    TimeElement(
                        start_time=datetime.time(hour=6),
                        end_time=datetime.time(hour=22),
                        end_time_on_next_day=False,
                        resource_state=State.WITH_RESERVATION,
                        periods=[],
                    ),
                ],
            },
        ]


@freezegun.freeze_time("2021-10-12T12:00:00Z")
@patch("opening_hours.utils.opening_hours_client.get_opening_hours")
@patch(
    "opening_hours.hours.get_periods_for_resource", return_value=get_mocked_periods()
)
class ReservationCreateTestCase(ReservationTestCaseBase):
    def get_create_query(self):
        return """
            mutation createReservation($input: ReservationCreateMutationInput!) {
                createReservation(input: $input) {
                    reservation {
                        pk
                        priority
                        calendarUrl
                    }
                    errors {
                        field
                        messages
                    }
                }
            }
        """

    def get_valid_input_data(self):
        return {
            "name": "Test reservation",
            "description": "Test description",
            "begin": datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ"),
            "end": (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime(
                "%Y%m%dT%H%M%SZ"
            ),
            "reservationUnitPks": [self.reservation_unit.pk],
        }

    def test_creating_reservation_succeed(self, mock_periods, mock_opening_hours):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        self._client.force_login(self.regular_joe)
        input_data = self.get_valid_input_data()
        response = self.query(self.get_create_query(), input_data=input_data)
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("createReservation").get("reservation").get("pk")
        ).is_not_none()
        pk = content.get("data").get("createReservation").get("reservation").get("pk")
        reservation = Reservation.objects.get(id=pk)
        assert_that(reservation).is_not_none()
        assert_that(reservation.user).is_equal_to(self.regular_joe)
        assert_that(reservation.state).is_equal_to(STATE_CHOICES.CREATED)
        assert_that(reservation.priority).is_equal_to(PRIORITY_CONST.PRIORITY_MEDIUM)
        assert_that(reservation.name).is_equal_to(input_data["name"])
        assert_that(reservation.description).is_equal_to(input_data["description"])

    def test_creating_reservation_without_name_and_description_succeeds(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        self._client.force_login(self.regular_joe)
        input_data = self.get_valid_input_data()
        input_data.pop("name")
        input_data.pop("description")
        response = self.query(self.get_create_query(), input_data=input_data)
        content = json.loads(response.content)
        assert_that(content.get("errors")).is_none()
        assert_that(Reservation.objects.exists()).is_true()

    def test_creating_reservation_with_pk_fails(self, mock_periods, mock_opening_hours):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        self._client.force_login(self.regular_joe)
        input_data = self.get_valid_input_data()
        input_data["pk"] = 9999
        response = self.query(self.get_create_query(), input_data=input_data)
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_not_none()
        assert_that(Reservation.objects.exists()).is_false()

    def test_create_fails_when_overlapping_reservation(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        ReservationFactory(
            reservation_unit=[self.reservation_unit],
            begin=datetime.datetime.now(),
            end=datetime.datetime.now() + datetime.timedelta(hours=2),
            state=STATE_CHOICES.CONFIRMED,
        )

        self._client.force_login(self.regular_joe)
        response = self.query(
            self.get_create_query(), input_data=self.get_valid_input_data()
        )
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")[0]["messages"]
        ).contains("Overlapping reservations are not allowed.")

    def test_create_fails_when_buffer_time_overlaps_reservation_before(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        begin = datetime.datetime.now() - datetime.timedelta(hours=2)
        end = begin + datetime.timedelta(hours=1)
        ReservationFactory(
            reservation_unit=[self.reservation_unit],
            begin=begin,
            end=end,
            buffer_time_after=datetime.timedelta(hours=1, minutes=1),
            state=STATE_CHOICES.CONFIRMED,
        )

        self._client.force_login(self.regular_joe)
        response = self.query(
            self.get_create_query(), input_data=self.get_valid_input_data()
        )
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")[0]["messages"][0]
        ).contains("before this has buffer time which overlaps this reservation.")

    def test_create_fails_when_buffer_time_overlaps_reservation_after(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        begin = datetime.datetime.now() + datetime.timedelta(hours=2)
        end = begin + datetime.timedelta(hours=1)
        ReservationFactory(
            reservation_unit=[self.reservation_unit],
            begin=begin,
            end=end,
            buffer_time_before=datetime.timedelta(hours=1, minutes=1),
            state=STATE_CHOICES.CONFIRMED,
        )

        self._client.force_login(self.regular_joe)
        response = self.query(
            self.get_create_query(), input_data=self.get_valid_input_data()
        )
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")[0]["messages"][0]
        ).contains("after this has buffer time which overlaps this reservation.")

    def test_create_fails_when_reservation_unit_buffer_time_overlaps_with_existing_reservation_before(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        self.reservation_unit.buffer_time_between_reservations = datetime.timedelta(
            hours=1, minutes=1
        )
        self.reservation_unit.save()
        begin = datetime.datetime.now() - datetime.timedelta(hours=2)
        end = begin + datetime.timedelta(hours=1)
        ReservationFactory(
            reservation_unit=[self.reservation_unit],
            begin=begin,
            end=end,
            state=STATE_CHOICES.CONFIRMED,
        )

        self._client.force_login(self.regular_joe)
        response = self.query(
            self.get_create_query(), input_data=self.get_valid_input_data()
        )
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")[0]["messages"][0]
        ).contains(
            "Reservation unit buffer time between reservations overlaps with current begin time."
        )

    def test_create_fails_when_reservation_unit_buffer_time_overlaps_with_existing_reservation_after(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        self.reservation_unit.buffer_time_between_reservations = datetime.timedelta(
            hours=1, minutes=1
        )
        self.reservation_unit.save()
        begin = datetime.datetime.now() + datetime.timedelta(hours=2)
        end = begin + datetime.timedelta(hours=1)
        ReservationFactory(
            reservation_unit=[self.reservation_unit],
            begin=begin,
            end=end,
            state=STATE_CHOICES.CONFIRMED,
        )

        self._client.force_login(self.regular_joe)
        response = self.query(
            self.get_create_query(), input_data=self.get_valid_input_data()
        )
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")[0]["messages"][0]
        ).contains(
            "Reservation unit buffer time between reservations overlaps with current end time."
        )

    def test_create_fails_when_reservation_unit_closed_on_selected_time(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        input_data = self.get_valid_input_data()
        input_data["begin"] = (
            datetime.datetime.now() - datetime.timedelta(days=1)
        ).strftime("%Y%m%dT%H%M%SZ")
        input_data["end"] = (
            datetime.datetime.now() - datetime.timedelta(hours=23)
        ).strftime("%Y%m%dT%H%M%SZ")

        self._client.force_login(self.regular_joe)
        response = self.query(self.get_create_query(), input_data=input_data)
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")[0]["messages"][0]
        ).contains("Reservation unit is not open within desired reservation time.")

    def test_create_fails_when_reservation_unit_in_open_application_round(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        ApplicationRoundFactory(
            reservation_units=[self.reservation_unit],
            reservation_period_begin=datetime.date.today(),
            reservation_period_end=datetime.date.today() + datetime.timedelta(days=10),
        )

        self._client.force_login(self.regular_joe)
        response = self.query(
            self.get_create_query(), input_data=self.get_valid_input_data()
        )
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")[0]["messages"][0]
        ).contains("One or more reservation units are in open application round.")

    def test_create_fails_when_reservation_unit_max_reservation_duration_exceeds(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        self.reservation_unit.max_reservation_duration = datetime.timedelta(minutes=30)
        self.reservation_unit.save()

        self._client.force_login(self.regular_joe)
        response = self.query(
            self.get_create_query(), input_data=self.get_valid_input_data()
        )
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")[0]["messages"][0]
        ).contains(
            "Reservation duration exceeds one or more reservation unit's maximum duration."
        )

    def test_create_fails_when_reservation_unit_min_reservation_duration_subsides(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        self.reservation_unit.max_reservation_duration = None
        self.reservation_unit.min_reservation_duration = datetime.timedelta(hours=2)
        self.reservation_unit.save()

        self._client.force_login(self.regular_joe)
        response = self.query(
            self.get_create_query(), input_data=self.get_valid_input_data()
        )
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("createReservation").get("errors")[0]["messages"][0]
        ).contains(
            "Reservation duration less than one or more reservation unit's minimum duration."
        )

    def test_create_fails_when_not_logged_in(self, mock_periods, mock_opening_hours):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        response = self.query(
            self.get_create_query(), input_data=self.get_valid_input_data()
        )
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_not_none()
        assert_that(content.get("errors")[0].get("message")).is_equal_to(
            "No permission to mutate"
        )


@freezegun.freeze_time("2021-10-12T12:00:00Z")
@patch("opening_hours.utils.opening_hours_client.get_opening_hours")
@patch(
    "opening_hours.hours.get_periods_for_resource", return_value=get_mocked_periods()
)
class ReservationUpdateTestCase(ReservationTestCaseBase):
    def setUp(self):
        super().setUp()
        self.reservation_begin = datetime.datetime.now(tz=get_default_timezone())
        self.reservation_end = datetime.datetime.now(
            tz=get_default_timezone()
        ) + datetime.timedelta(hours=1)
        self.reservation = ReservationFactory(
            reservation_unit=[self.reservation_unit],
            begin=self.reservation_begin,
            end=self.reservation_end,
            state=STATE_CHOICES.REQUESTED,
            user=self.regular_joe,
            priority=100,
        )

    def get_update_query(self):
        return """
            mutation updateReservation($input: ReservationUpdateMutationInput!) {
                updateReservation(input: $input) {
                    reservation {
                        pk
                        priority
                        calendarUrl
                    }
                    errors {
                        field
                        messages
                    }
                }
            }
        """

    def get_valid_update_data(self):
        return {
            "pk": self.reservation.pk,
            "priority": 200,
            "begin": (self.reservation_begin + datetime.timedelta(hours=1)).strftime(
                "%Y%m%dT%H%M%SZ"
            ),
            "end": (self.reservation_end + datetime.timedelta(hours=1)).strftime(
                "%Y%m%dT%H%M%SZ"
            ),
        }

    def test_updating_reservation_succeed(self, mock_periods, mock_opening_hours):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        self._client.force_login(self.regular_joe)
        response = self.query(
            self.get_update_query(), input_data=self.get_valid_update_data()
        )
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("updateReservation").get("reservation").get("pk")
        ).is_not_none()
        pk = content.get("data").get("updateReservation").get("reservation").get("pk")
        reservation = Reservation.objects.get(id=pk)
        assert_that(reservation).is_not_none()
        assert_that(reservation.user).is_equal_to(self.regular_joe)
        assert_that(reservation.state).is_equal_to(STATE_CHOICES.REQUESTED)
        assert_that(reservation.priority).is_equal_to(
            self.get_valid_update_data()["priority"]
        )
        assert_that(reservation.begin).is_equal_to(
            self.reservation_begin + datetime.timedelta(hours=1)
        )
        assert_that(reservation.end).is_equal_to(
            (self.reservation_end + datetime.timedelta(hours=1))
        )

    def test_updating_reservation_with_pk_fails(self, mock_periods, mock_opening_hours):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        new_pk = 9999
        self._client.force_login(self.regular_joe)
        input_data = self.get_valid_update_data()
        input_data["pk"] = new_pk
        response = self.query(self.get_update_query(), input_data=input_data)
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_not_none()
        assert_that(Reservation.objects.filter(pk=new_pk)).is_false()

    def test_update_fails_when_overlapping_reservation(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        ReservationFactory(
            reservation_unit=[self.reservation_unit],
            begin=datetime.datetime.now(),
            end=datetime.datetime.now() + datetime.timedelta(hours=2),
            state=STATE_CHOICES.CONFIRMED,
        )

        self._client.force_login(self.regular_joe)
        response = self.query(
            self.get_update_query(), input_data=self.get_valid_update_data()
        )
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")[0]["messages"]
        ).contains("Overlapping reservations are not allowed.")

    def test_update_fails_when_buffer_time_overlaps_reservation_before(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        begin = datetime.datetime.now() - datetime.timedelta(hours=2)
        end = begin + datetime.timedelta(hours=1)
        ReservationFactory(
            reservation_unit=[self.reservation_unit],
            begin=begin,
            end=end,
            buffer_time_after=datetime.timedelta(hours=1, minutes=1),
            state=STATE_CHOICES.CONFIRMED,
        )

        self._client.force_login(self.regular_joe)
        response = self.query(
            self.get_update_query(),
            input_data={"pk": self.reservation.id, "priority": 200},
        )
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")[0]["messages"][0]
        ).contains("before this has buffer time which overlaps this reservation.")
        self.reservation.refresh_from_db()
        assert_that(self.reservation.priority).is_equal_to(100)

    def test_update_fails_when_buffer_time_overlaps_reservation_after(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        begin = datetime.datetime.now() + datetime.timedelta(hours=2)
        end = begin + datetime.timedelta(hours=1)
        ReservationFactory(
            reservation_unit=[self.reservation_unit],
            begin=begin,
            end=end,
            buffer_time_before=datetime.timedelta(hours=1, minutes=1),
            state=STATE_CHOICES.CONFIRMED,
        )

        self._client.force_login(self.regular_joe)
        response = self.query(
            self.get_update_query(), input_data=self.get_valid_update_data()
        )
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")[0]["messages"][0]
        ).contains("after this has buffer time which overlaps this reservation.")

    def test_update_fails_when_reservation_unit_buffer_time_overlaps_with_existing_reservation_before(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        self.reservation_unit.buffer_time_between_reservations = datetime.timedelta(
            hours=1, minutes=1
        )
        self.reservation_unit.save()
        begin = self.reservation_begin - datetime.timedelta(hours=2)
        end = begin + datetime.timedelta(hours=1)
        ReservationFactory(
            reservation_unit=[self.reservation_unit],
            begin=begin,
            end=end,
            state=STATE_CHOICES.CONFIRMED,
        )

        self._client.force_login(self.regular_joe)
        input_data = self.get_valid_update_data()
        input_data.pop("begin")
        input_data.pop("end")
        response = self.query(self.get_update_query(), input_data=input_data)
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")[0]["messages"][0]
        ).contains(
            "Reservation unit buffer time between reservations overlaps with current begin time."
        )

    def test_update_fails_when_reservation_unit_buffer_time_overlaps_with_existing_reservation_after(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        self.reservation_unit.buffer_time_between_reservations = datetime.timedelta(
            hours=1, minutes=1
        )
        self.reservation_unit.save()
        begin = datetime.datetime.now() + datetime.timedelta(hours=2)
        end = begin + datetime.timedelta(hours=1)
        ReservationFactory(
            reservation_unit=[self.reservation_unit],
            begin=begin,
            end=end,
            state=STATE_CHOICES.CONFIRMED,
        )

        self._client.force_login(self.regular_joe)
        response = self.query(
            self.get_update_query(), input_data=self.get_valid_update_data()
        )
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")[0]["messages"][0]
        ).contains(
            "Reservation unit buffer time between reservations overlaps with current end time."
        )

    def test_update_fails_when_reservation_unit_closed_on_selected_time(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        input_data = self.get_valid_update_data()
        input_data["begin"] = (
            datetime.datetime.now() - datetime.timedelta(days=1)
        ).strftime("%Y%m%dT%H%M%SZ")
        input_data["end"] = (
            datetime.datetime.now() - datetime.timedelta(hours=23)
        ).strftime("%Y%m%dT%H%M%SZ")

        self._client.force_login(self.regular_joe)
        response = self.query(self.get_update_query(), input_data=input_data)
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")[0]["messages"][0]
        ).contains("Reservation unit is not open within desired reservation time.")

    def test_update_fails_when_reservation_unit_in_open_application_round(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        ApplicationRoundFactory(
            reservation_units=[self.reservation_unit],
            reservation_period_begin=datetime.date.today(),
            reservation_period_end=datetime.date.today() + datetime.timedelta(days=10),
        )

        self._client.force_login(self.regular_joe)
        response = self.query(
            self.get_update_query(), input_data=self.get_valid_update_data()
        )
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")[0]["messages"][0]
        ).contains("One or more reservation units are in open application round.")

    def test_update_fails_when_reservation_unit_max_reservation_duration_exceeds(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        self.reservation_unit.max_reservation_duration = datetime.timedelta(minutes=30)
        self.reservation_unit.save()

        self._client.force_login(self.regular_joe)
        response = self.query(
            self.get_update_query(), input_data=self.get_valid_update_data()
        )
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")[0]["messages"][0]
        ).contains(
            "Reservation duration exceeds one or more reservation unit's maximum duration."
        )

    def test_update_fails_when_reservation_unit_min_reservation_duration_subsides(
        self, mock_periods, mock_opening_hours
    ):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        self.reservation_unit.max_reservation_duration = None
        self.reservation_unit.min_reservation_duration = datetime.timedelta(hours=2)
        self.reservation_unit.save()

        self._client.force_login(self.regular_joe)
        response = self.query(
            self.get_update_query(), input_data=self.get_valid_update_data()
        )
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")
        ).is_not_none()
        assert_that(
            content.get("data").get("updateReservation").get("errors")[0]["messages"][0]
        ).contains(
            "Reservation duration less than one or more reservation unit's minimum duration."
        )

    def test_update_fails_when_not_permission(self, mock_periods, mock_opening_hours):
        mock_opening_hours.return_value = self.get_mocked_opening_hours()
        citizen = get_user_model().objects.create(
            username="citzen",
            first_name="citi",
            last_name="zen",
            email="zen.citi@foo.com",
        )
        res = ReservationFactory(
            reservation_unit=[self.reservation_unit],
            begin=datetime.datetime.now(),
            end=datetime.datetime.now() + datetime.timedelta(hours=2),
            state=STATE_CHOICES.CREATED,
            user=citizen,
        )
        input_data = self.get_valid_update_data()
        input_data["pk"] = res.pk
        self._client.force_login(self.regular_joe)
        response = self.query(self.get_update_query(), input_data=input_data)
        content = json.loads(response.content)

        assert_that(content.get("errors")).is_not_none()
        assert_that(content.get("errors")[0].get("message")).is_equal_to(
            "No permission to mutate"
        )
