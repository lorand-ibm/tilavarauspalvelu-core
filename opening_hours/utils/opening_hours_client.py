import datetime

from django.conf import settings

from opening_hours.hours import TimeElement, get_opening_hours


class OpeningHoursClient:
    def __init__(
        self,
        resources: [str],
        start: datetime.date,
        end: datetime.date,
        single=False,
    ):
        if single:
            resources = [str(resources)]
        self.start = start
        self.end = end

        self.resources = {}

        self.resources = {
            f"{settings.HAUKI_ORIGIN_ID}:{resource_id}": resource_id
            for resource_id in resources
        }
        self.opening_hours = {}
        self._init_opening_hours_structure()

        self._fetch_opening_hours(resources, start, end)

    def _init_opening_hours_structure(self):
        """Opening hours structure is:
        opening_hours = {
            resource_id: {
                            datetime.date: [TimeElement, TimeElement, ...],
                            ....
                        },
            resource_id: { datetime.date: [TimeElement, ...
            ...
        }
        """
        self.opening_hours = {res_id: {} for k, res_id in self.resources.items()}
        running_date = self.start
        while running_date <= self.end:
            for k, res_id in self.resources.items():
                self.opening_hours[res_id].update({running_date: []})
            running_date += datetime.timedelta(days=1)

    def _fetch_opening_hours(
        self, resources: [str], start: datetime.date, end: datetime.date
    ):
        for hour in get_opening_hours(resources, start, end):
            res_id = self.resources[hour["resource_id"]]
            self.opening_hours[res_id][hour["date"]].extend(hour["times"])

    def refresh_opening_hours(self):
        self._init_opening_hours_structure()
        resources = [res_id for k, res_id in self.resources.items()]
        self._fetch_opening_hours(resources, self.start, self.end)

    def get_opening_hours_for_resource(self, resource, date) -> [TimeElement]:
        resource = self.opening_hours.get(resource, {})
        times = resource.get(date, [])
        return times

    def is_resource_open(
        self, resource: str, start_time: datetime.datetime, end_time: datetime.datetime
    ) -> bool:
        times = self.get_opening_hours_for_resource(resource, start_time.date())
        for time in times:
            if (
                time.start_time <= start_time.time()
                and time.end_time >= end_time.time()
                and (time.end_time_on_next_day or end_time.date() == start_time.date())
            ):
                return True
        return False

    def next_opening_times(
        self, resource: str, date: datetime.date
    ) -> (datetime.date, [TimeElement]):
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
