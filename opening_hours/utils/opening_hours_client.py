import datetime
from typing import Dict, List, Union

import pytz
from django.conf import settings
from django.utils.timezone import get_default_timezone

from opening_hours.decorators import datetime_args_to_default_timezone
from opening_hours.hours import (
    Period,
    TimeElement,
    get_opening_hours,
    get_periods_for_resource,
)

TIMEZONE = get_default_timezone()


class OpeningHours:
    start_time: datetime.datetime
    end_time: datetime.datetime
    resource_state: str
    periods: List[int]

    def __init__(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        resource_state: str,
        periods: List[int],
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.resource_state = resource_state
        self.periods = periods

    @classmethod
    def get_opening_hours_class_from_time_element(
        cls,
        time_element: TimeElement,
        date: datetime.date,
        timezone: Union[
            type(pytz.UTC), pytz.tzinfo.DstTzInfo, pytz.tzinfo.StaticTzInfo
        ],
    ):
        start_time = timezone.localize(
            datetime.datetime(
                date.year,
                date.month,
                date.day,
                time_element.start_time.hour,
                time_element.end_time.minute,
            )
        )
        if time_element.end_time_on_next_day:
            date += datetime.timedelta(days=1)
        end_time = timezone.localize(
            datetime.datetime(
                date.year,
                date.month,
                date.day,
                time_element.end_time.hour,
                time_element.end_time.minute,
            )
        )
        return OpeningHours(
            start_time=start_time.astimezone(TIMEZONE),
            end_time=end_time.astimezone(TIMEZONE),
            resource_state=time_element.resource_state,
            periods=time_element.periods,
        )


class OpeningHoursClient:
    def __init__(
        self,
        resources: [str],
        start: datetime.date,
        end: datetime.date,
        single=False,
        init_periods=False,
        init_opening_hours=True,
        hauki_origin_id=None,
    ):
        if single:
            resources = [str(resources)]
        self.start = start
        self.end = end

        if hauki_origin_id:
            self.hauki_origin_id = hauki_origin_id
        else:
            self.hauki_origin_id = settings.HAUKI_ORIGIN_ID

        self.resources = {}

        self.resources = resources
        self.opening_hours = {}
        if init_opening_hours:
            self._init_opening_hours_structure()
            self._fetch_opening_hours(start, end)

        self.periods = {}
        for resource in resources:
            self.periods[resource] = []
        if init_periods:
            for resource in resources:
                periods = get_periods_for_resource(resource)
                for period in periods:
                    self.periods[resource].append(period)

    def _init_opening_hours_structure(self):
        """Opening hours structure is:
        opening_hours = {
            resource_id: {
                            datetime.date: [OpeningHours, OpeningHours, ...],
                            ....
                        },
            resource_id: { datetime.date: [OpeningHours, ...
            ...
        }
        """
        self.opening_hours = {res_id: {} for res_id in self.resources}
        running_date = self.start
        while running_date <= self.end:
            for res_id in self.resources:
                self.opening_hours[res_id].update({running_date: []})
            running_date += datetime.timedelta(days=1)

    def _fetch_opening_hours(self, start: datetime.date, end: datetime.date):
        for hour in get_opening_hours(self.resources, start, end, self.hauki_origin_id):
            res_id = hour["origin_id"]
            timezone = hour["timezone"]
            date = hour["date"]
            opening_hours = []
            for time in hour["times"]:
                opening_times = OpeningHours.get_opening_hours_class_from_time_element(
                    time, date, timezone
                )
                opening_hours.append(opening_times)

            self.opening_hours[res_id][date].extend(opening_hours)

    def refresh_opening_hours(self):
        self._init_opening_hours_structure()
        self._fetch_opening_hours(self.start, self.end)

    def get_opening_hours_for_resource(self, resource, date) -> [TimeElement]:
        resource = self.opening_hours.get(resource, {})
        times = resource.get(date, [])
        return times

    def get_opening_hours_for_date_range(
        self, resource: str, date_start: datetime.date, date_end: datetime.date
    ) -> Dict[datetime.date, List[TimeElement]]:
        opening_hours = {
            date: times
            for date, times in self.opening_hours.get(resource, {}).items()
            if date >= date_start and date <= date_end and times
        }
        return opening_hours

    def get_resource_periods(self, resource) -> List[Period]:
        return self.periods.get(resource)

    @datetime_args_to_default_timezone
    def is_resource_open(
        self, resource: str, start_time: datetime.datetime, end_time: datetime.datetime
    ) -> bool:
        times = self.get_opening_hours_for_resource(resource, start_time.date())
        for time in times:
            if time.start_time <= start_time and time.end_time >= end_time:
                return True
        return False

    def next_opening_times(
        self, resource: str, date: datetime.date
    ) -> (datetime.date, [OpeningHours]):
        times_for_resource = self.opening_hours.get(resource, {})
        times = times_for_resource.get(date)

        running_date = date
        while not times:
            dates = [dt for dt in times_for_resource.keys() if dt > running_date]
            running_date = min(dates) if dates else None
            if not running_date:
                break
            times = times_for_resource.get(running_date)

        return running_date, times
