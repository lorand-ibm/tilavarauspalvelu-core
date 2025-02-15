import datetime

import pytest
from assertpy import assert_that

from applications.models import APPLICANT_TYPES, CUSTOMER_TYPES


@pytest.mark.django_db
def test_getting_occurences(recurring_application_event, scheduled_for_tuesday):
    occurrences = recurring_application_event.get_all_occurrences()
    dates = []
    start = datetime.datetime(2020, 1, 7, 10, 0)
    delta = datetime.timedelta(days=7)
    while start <= datetime.datetime(2020, 2, 25, 10, 0):
        dates.append(start)
        start += delta
    assert occurrences[scheduled_for_tuesday.id].occurrences == dates
    assert occurrences[scheduled_for_tuesday.id].weekday == scheduled_for_tuesday.day


@pytest.mark.django_db
def test_getting_not_scheduled_occurrences_for_not_accepted_result(
    recurring_application_event, scheduled_for_tuesday, result_scheduled_for_tuesday
):
    result_scheduled_for_tuesday.accepted = False
    occurrences = recurring_application_event.get_not_scheduled_occurrences()

    assert_that(occurrences[scheduled_for_tuesday.id].occurrences).is_length(8)


@pytest.mark.django_db
def test_getting_not_scheduled_occurrences_for_accepted_result(
    recurring_application_event, scheduled_for_tuesday, result_scheduled_for_tuesday
):
    result_scheduled_for_tuesday.accepted = True
    result_scheduled_for_tuesday.save()
    occurrences = recurring_application_event.get_not_scheduled_occurrences()

    assert_that(hasattr(occurrences, f"{scheduled_for_tuesday.id}")).is_false()


@pytest.mark.django_db
def test_getting_not_scheduled_occurrences_without_schedule_result(
    recurring_application_event, scheduled_for_tuesday
):
    occurrences = recurring_application_event.get_not_scheduled_occurrences()

    assert_that(hasattr(occurrences, f"{scheduled_for_tuesday.id}")).is_false()


@pytest.mark.django_db
def test_should_filter_to_baskets_by_purpose(
    default_application_round, application_round_basket_one, recurring_application_event
):
    events_by_baskets = default_application_round.get_application_events_by_basket()

    assert events_by_baskets == {
        application_round_basket_one.id: [recurring_application_event]
    }


@pytest.mark.django_db
def test_should_exclude_if_purpose_does_not_match(
    default_application_round,
    application_round_basket_one,
    recurring_application_event,
    purpose_two,
):
    application_round_basket_one.purposes.set([purpose_two])
    application_round_basket_one.save()

    events_by_baskets = default_application_round.get_application_events_by_basket()

    assert events_by_baskets == {application_round_basket_one.id: []}


@pytest.mark.django_db
def test_should_include_if_basket_has_no_purposes(
    default_application_round,
    application_round_basket_one,
    recurring_application_event,
    purpose_two,
):
    application_round_basket_one.purposes.set([])
    application_round_basket_one.save()

    events_by_baskets = default_application_round.get_application_events_by_basket()

    assert events_by_baskets == {
        application_round_basket_one.id: [recurring_application_event]
    }


@pytest.mark.django_db
def test_should_filter_by_age_group(
    default_application_round,
    application_round_basket_one,
    recurring_application_event,
    purpose_two,
    five_to_ten_age_group,
):
    application_round_basket_one.age_groups.set([five_to_ten_age_group])
    application_round_basket_one.save()
    recurring_application_event.age_group = five_to_ten_age_group
    recurring_application_event.save()
    events_by_baskets = default_application_round.get_application_events_by_basket()

    assert events_by_baskets == {
        application_round_basket_one.id: [recurring_application_event]
    }


@pytest.mark.django_db
def test_should_test_should_exclude_if_age_group_does_not_match(
    default_application_round,
    application_round_basket_one,
    recurring_application_event,
    purpose_two,
    five_to_ten_age_group,
    fifty_to_eighty_age_group,
):
    application_round_basket_one.age_groups.set([five_to_ten_age_group])
    application_round_basket_one.save()
    recurring_application_event.age_group = fifty_to_eighty_age_group
    recurring_application_event.save()

    events_by_baskets = default_application_round.get_application_events_by_basket()

    assert events_by_baskets == {application_round_basket_one.id: []}


@pytest.mark.django_db
def test_event_can_belong_to_multiple_baskets(
    default_application_round,
    application_round_basket_one,
    application_round_basket_two,
    recurring_application_event,
):
    events_by_baskets = default_application_round.get_application_events_by_basket()

    assert events_by_baskets == {
        application_round_basket_one.id: [recurring_application_event],
        application_round_basket_two.id: [recurring_application_event],
    }


@pytest.mark.django_db
def test_should_exclude_events_not_matching_application_round(
    default_application_round,
    second_application_round,
    application_round_basket_one,
    recurring_application_event,
    application_in_second_application_round,
):
    recurring_application_event.application = application_in_second_application_round
    recurring_application_event.save()

    events_by_baskets = default_application_round.get_application_events_by_basket()

    assert events_by_baskets == {application_round_basket_one.id: []}


@pytest.mark.django_db
def test_should_filter_to_baskets_by_home_city(
    default_application_round,
    application_round_basket_one,
    recurring_application_event,
    city_of_helsinki,
):
    application_round_basket_one.home_city = city_of_helsinki
    application_round_basket_one.save()
    recurring_application_event.application.home_city = city_of_helsinki
    recurring_application_event.application.save()

    events_by_baskets = default_application_round.get_application_events_by_basket()

    assert events_by_baskets == {
        application_round_basket_one.id: [recurring_application_event]
    }


@pytest.mark.django_db
def test_should_exclude_if_city_does_not_match(
    default_application_round,
    application_round_basket_one,
    recurring_application_event,
    city_of_helsinki,
    city_of_tampere,
):
    application_round_basket_one.home_city = city_of_helsinki
    application_round_basket_one.save()
    recurring_application_event.application.home_city = city_of_tampere
    recurring_application_event.application.save()

    events_by_baskets = default_application_round.get_application_events_by_basket()

    assert events_by_baskets == {application_round_basket_one.id: []}


@pytest.mark.django_db
def test_should_include_if_basket_has_no_home_city(
    default_application_round,
    application_round_basket_one,
    recurring_application_event,
    city_of_helsinki,
):
    recurring_application_event.application.home_city = city_of_helsinki
    recurring_application_event.application.save()

    events_by_baskets = default_application_round.get_application_events_by_basket()

    assert events_by_baskets == {
        application_round_basket_one.id: [recurring_application_event]
    }


@pytest.mark.parametrize(
    "applicant_customer_type",
    [
        (APPLICANT_TYPES.APPLICANT_TYPE_COMPANY, CUSTOMER_TYPES.CUSTOMER_TYPE_BUSINESS),
        (
            APPLICANT_TYPES.APPLICANT_TYPE_ASSOCIATION,
            CUSTOMER_TYPES.CUSTOMER_TYPE_NONPROFIT,
        ),
        (
            APPLICANT_TYPES.APPLICANT_TYPE_COMMUNITY,
            CUSTOMER_TYPES.CUSTOMER_TYPE_NONPROFIT,
        ),
        (
            APPLICANT_TYPES.APPLICANT_TYPE_INDIVIDUAL,
            CUSTOMER_TYPES.CUSTOMER_TYPE_INDIVIDUAL,
        ),
    ],
)
@pytest.mark.django_db
def test_should_filter_to_baskets_by_customer_type(
    applicant_customer_type,
    default_application_round,
    application_round_basket_one,
    recurring_application_event,
):
    applicant_type, customer_type = applicant_customer_type
    application_round_basket_one.customer_type = [customer_type]
    application_round_basket_one.save()
    recurring_application_event.application.applicant_type = applicant_type
    recurring_application_event.application.save()

    events_by_baskets = default_application_round.get_application_events_by_basket()

    assert events_by_baskets == {
        application_round_basket_one.id: [recurring_application_event]
    }


@pytest.mark.parametrize(
    "applicant_customer_type",
    [
        (
            APPLICANT_TYPES.APPLICANT_TYPE_COMPANY,
            [
                CUSTOMER_TYPES.CUSTOMER_TYPE_NONPROFIT,
                CUSTOMER_TYPES.CUSTOMER_TYPE_INDIVIDUAL,
            ],
        ),
        (
            APPLICANT_TYPES.APPLICANT_TYPE_ASSOCIATION,
            [
                CUSTOMER_TYPES.CUSTOMER_TYPE_BUSINESS,
                CUSTOMER_TYPES.CUSTOMER_TYPE_INDIVIDUAL,
            ],
        ),
        (
            APPLICANT_TYPES.APPLICANT_TYPE_COMMUNITY,
            [
                CUSTOMER_TYPES.CUSTOMER_TYPE_BUSINESS,
                CUSTOMER_TYPES.CUSTOMER_TYPE_INDIVIDUAL,
            ],
        ),
        (
            APPLICANT_TYPES.APPLICANT_TYPE_INDIVIDUAL,
            [
                CUSTOMER_TYPES.CUSTOMER_TYPE_NONPROFIT,
                CUSTOMER_TYPES.CUSTOMER_TYPE_BUSINESS,
            ],
        ),
    ],
)
@pytest.mark.django_db
def test_should_exclude_if_customer_type_does_not_match(
    applicant_customer_type,
    default_application_round,
    application_round_basket_one,
    recurring_application_event,
):
    applicant_type, customer_type = applicant_customer_type
    application_round_basket_one.customer_type = customer_type
    application_round_basket_one.save()
    recurring_application_event.application.applicant_type = applicant_type
    recurring_application_event.application.save()

    events_by_baskets = default_application_round.get_application_events_by_basket()

    assert events_by_baskets == {application_round_basket_one.id: []}


@pytest.mark.parametrize(
    "applicant_type",
    [
        APPLICANT_TYPES.APPLICANT_TYPE_COMPANY,
        APPLICANT_TYPES.APPLICANT_TYPE_ASSOCIATION,
        APPLICANT_TYPES.APPLICANT_TYPE_COMMUNITY,
        APPLICANT_TYPES.APPLICANT_TYPE_INDIVIDUAL,
    ],
)
@pytest.mark.django_db
def test_should_include_if_no_customer_type(
    applicant_type,
    default_application_round,
    application_round_basket_one,
    recurring_application_event,
):
    recurring_application_event.application.applicant_type = applicant_type
    recurring_application_event.application.save()

    events_by_baskets = default_application_round.get_application_events_by_basket()

    assert events_by_baskets == {
        application_round_basket_one.id: [recurring_application_event]
    }
