from datetime import date, datetime
from json import load
from pathlib import Path
from typing import Iterable, Optional

from django.core.management.base import BaseCommand

from reservation_units.models import (
    Day,
    Equipment,
    EquipmentCategory,
    Period,
    Purpose,
    ReservationUnit,
    ReservationUnitType,
)
from reservations.models import Reservation
from resources.models import Resource
from spaces.models import Space, Unit


class Command(BaseCommand):
    help = "Imports Respa data from the given JSON file."

    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="Path to the JSON file.")
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Do not create any model instances.",
        )

    def handle(self, *args, **options) -> None:
        json_path = options.get("file")
        dry_run = options.get("dry_run")
        if dry_run:
            self.stdout.write("Dry run enabled; not creating any instances.")
        self.stdout.write(f"Importing from {json_path}.")
        _delete_existing_data()
        _import_everything(json_path, save=not dry_run)
        self.stdout.write(self.style.SUCCESS("Import successful."))


def _delete_existing_data() -> None:
    Purpose.objects.all().delete()
    Unit.objects.all().delete()
    Space.objects.all().delete()
    Resource.objects.all().delete()
    ReservationUnitType.objects.all().delete()
    EquipmentCategory.objects.all().delete()
    Equipment.objects.all().delete()
    ReservationUnit.objects.all().delete()
    Reservation.objects.all().delete()
    Period.objects.all().delete()
    Day.objects.all().delete()


# Depends on Unit, District, Building
def _import_spaces(data: dict, unit_map: dict, save: bool = False) -> dict:
    pk_map = {}
    space_types = _find_space_types(data)
    for obj in data["resources"]:
        if obj["type"] not in space_types:
            continue
        instance = Space(
            name=obj["name"],
            unit_id=unit_map[obj["unit"]],
            surface_area=obj["area"],
            max_persons=obj["people_capacity"],
            # parent=???,
            # code=???,
            # district_id=???,
            # building_id=???,
            # terms_of_use=???,
        )
        if save:
            instance.save()
        pk_map[obj["pk"]] = instance.pk
    return pk_map


def _import_resources(data: dict, save: bool = False) -> dict:
    non_space_types = _find_non_space_types(data)
    pk_map = {}
    for obj in data["resources"]:
        if obj["type"] not in non_space_types:
            continue  # Spaces have their own model
        instance = Resource(
            name=obj["name"],
            description=obj["description"],
            is_draft=not obj["public"],
            # location_type=???,
            # space=???,
            # buffer_time_before=???,
            # buffer_time_after=???,
        )
        if save:
            instance.save()
        pk_map[obj["pk"]] = instance.pk
    return pk_map


# Depends on ReservationUnit
def _import_periods(data: dict, reservation_unit_map: dict, save: bool = False) -> dict:
    pk_map = {}
    for obj in data["periods"]:
        reservation_unit = (
            reservation_unit_map[obj["resource"]]
            if obj["resource"] is not None
            else None
        )
        instance = Period(
            reservation_unit_id=reservation_unit,
            start=_date_or_none(obj["start"]),
            end=_date_or_none(obj["end"]),
            name=obj["name"],
            description=obj["description"],
            closed=obj["closed"],
        )
        if save:
            instance.save()
        pk_map[obj["pk"]] = instance.pk
    return pk_map


# Depends on Period
def _import_days(data: dict, period_map: dict, save: bool = False) -> dict:
    pk_map = {}
    for obj in data["days"]:
        instance = Day(
            period_id=period_map[obj["period"]],
            weekday=obj["weekday"],
            opens=obj["opens"],
            closes=obj["closes"],
        )
        if save:
            instance.save()
        pk_map[obj["pk"]] = instance.pk
    return pk_map


# No dependencies
def _import_purposes(data: dict, save: bool = False) -> dict:
    pk_map = {}
    for obj in data["purposes"]:
        instance = Purpose(name=obj["name"])
        if save:
            instance.save()
        pk_map[obj["pk"]] = instance.pk
    return pk_map


# No dependencies
def _import_units(data: dict, save: bool = False) -> dict:
    pk_map = {}
    for obj in data["units"]:
        instance = Unit(
            tprek_id=obj["pk"],
            name=obj["name"],
            description=obj["description"],
            web_page=obj["www_url"] if obj["www_url"] is not None else "",
            email=obj["email"],
            phone=obj["phone"] if obj["phone"] is not None else "",
            # short_description=???
        )
        if save:
            instance.save()
        pk_map[obj["pk"]] = instance.pk
    return pk_map


# No dependencies
def _import_reservation_unit_types(data: dict, save: bool = False) -> dict:
    pk_map = {}
    # Here we assume that Respa's ResourceType model corresponds to our ReservationUnitType
    for obj in data["resource_types"]:
        instance = ReservationUnitType(name=obj["name"])
        if save:
            instance.save()
        pk_map[obj["pk"]] = instance.pk
    return pk_map


# Depends on Space, Resource, Service, Purpose, ReservationUnitType, Equipment, Unit
def _import_reservation_units(
    data: dict,
    space_map: dict,
    resource_map: dict,
    purpose_map: dict,
    reservation_unit_type_map: dict,
    equipment_map: dict,
    unit_map: dict,
    save: bool = False,
) -> dict:
    pk_map = {}
    space_types = _find_space_types(data)
    # Here we assume that Respa's Reservation model corresponds to ReservationUnit
    for obj in data["resources"]:
        instance = ReservationUnit(
            name=obj["name"],
            description=obj["description"],
            reservation_unit_type_id=reservation_unit_type_map[obj["type"]],
            unit_id=unit_map[obj["unit"]],
            contact_information=obj["responsible_contact_info"],
            is_draft=not obj["public"],
            max_persons=obj["people_capacity"],
            surface_area=obj["area"],
            # keyword_groups=???,
            # services=???,
            # require_introduction=???,
            # terms_of_use=???,
            # max_reservation_duration=???,
            # min_reservation_duration=???,
            # buffer_time_between_reservations=???,
        )
        if obj["type"] in space_types:
            spaces = [space_map[obj["pk"]]]
            resources = []
        else:
            spaces = []
            resources = [resource_map[obj["pk"]]]
        purposes = [purpose_map[pk] for pk in obj["purposes"]]
        equipments = [equipment_map[pk] for pk in obj["equipment"]]
        if save:
            instance.save()
            instance.resources.set(resources)
            instance.spaces.set(spaces)
            instance.purposes.set(purposes)
            instance.equipments.set(equipments)
        pk_map[obj["pk"]] = instance.pk
    return pk_map


# Depends on User
def _import_reservations(
    data: dict, reservation_unit_map: dict, save: bool = False
) -> dict:
    pk_map = {}
    for obj in data["reservations"]:
        instance = Reservation(
            state=obj["state"],
            begin=_datetime_or_none(obj["begin"]),
            end=_datetime_or_none(obj["end"]),
            num_persons=obj["number_of_participants"],
            # priority=???,
            # user=???,
            # buffer_time_before=???,
            # buffer_time_after=???,
            # recurring_reservation=???,
        )
        if save:
            instance.save()
            instance.reservation_unit.set([reservation_unit_map[obj["resource"]]]),
        pk_map[obj["pk"]] = instance.pk
    return pk_map


# No dependencies
def _import_equipment_categories(data: dict, save: bool = False) -> dict:
    pk_map = {}
    for obj in data["equipment_categories"]:
        instance = EquipmentCategory(name=obj["name"])
        if save:
            instance.save()
        pk_map[obj["pk"]] = instance.pk
    return pk_map


# Depends on EquipmentCategory
def _import_equipment(
    data: dict, equipment_category_map: dict, save: bool = False
) -> dict:
    pk_map = {}
    for obj in data["equipment"]:
        instance = Equipment(
            name=obj["name"],
            category_id=equipment_category_map[obj["category"]],
        )
        if save:
            instance.save()
        pk_map[obj["pk"]] = instance.pk
    return pk_map


def _import_everything(path: str, save: bool = False) -> None:
    json_path = Path(path)
    json_file = json_path.open()
    json_data = load(json_file)

    purpose_map = _import_purposes(json_data, save)
    unit_map = _import_units(json_data, save)
    space_map = _import_spaces(json_data, unit_map, save)
    resource_map = _import_resources(json_data, save)
    reservation_unit_type_map = _import_reservation_unit_types(json_data, save)
    equipment_category_map = _import_equipment_categories(json_data, save)
    equipment_map = _import_equipment(json_data, equipment_category_map, save)

    reservation_unit_map = _import_reservation_units(
        json_data,
        space_map,
        resource_map,
        purpose_map,
        reservation_unit_type_map,
        equipment_map,
        unit_map,
        save,
    )

    _ = _import_reservations(json_data, reservation_unit_map, save)

    period_map = _import_periods(json_data, reservation_unit_map, save)
    _ = _import_days(json_data, period_map, save)


def _date_or_none(datestamp: Optional[str]) -> Optional[date]:
    return date.fromisoformat(datestamp) if datestamp is not None else None


def _datetime_or_none(timestamp: Optional[str]) -> Optional[datetime]:
    return datetime.fromisoformat(timestamp) if timestamp is not None else None


def _find_resource_types(data: dict) -> Iterable[str]:
    for obj in data["resource_types"]:
        yield obj["pk"]


def _find_space_types(data: dict) -> Iterable[str]:
    types = set()
    for obj in data["resource_types"]:
        if obj["main_type"] == "space":
            types.add(obj["pk"])
    return types


def _find_non_space_types(data: dict) -> Iterable[str]:
    types = set()
    for obj in data["resource_types"]:
        if obj["main_type"] != "space":
            types.add(obj["pk"])
    return types
