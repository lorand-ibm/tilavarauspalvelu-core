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


# Depends on Unit, District, Building
def _import_spaces(data: dict, unit_map: dict, save: bool = False) -> dict:
    pk_map = {}
    for obj in data["spaces"]:
        # obj:
        # {
        #   "pk": 1,
        #   "name_fi": "Joku tilaresurssi",
        #   "name_sv": null,
        #   "name_en": null,
        #   "unit_id": 1,
        #   "surface_area": null,
        #   "max_persons": null,
        #   "parent": null,
        #   "code": null,
        #   "district_id": null,
        #   "building_id": null,
        #   "terms_of_use_fi": null,
        #   "terms_of_use_sv": null,
        #   "terms_of_use_en": null
        # }
        instance = Space(
            name=obj["name_fi"],
            name_fi=obj["name_fi"],
            name_sv=obj["name_sv"],
            name_en=obj["name_en"],
            unit_id=unit_map[obj["unit_id"]],
            surface_area=obj["surface_area"],
            max_persons=obj["max_persons"],
            parent=obj["parent"],
            code=obj["code"] or "",
            district_id=obj["district_id"],
            building_id=obj["building_id"],
            terms_of_use=obj["terms_of_use_fi"],
            terms_of_use_fi=obj["terms_of_use_fi"],
            terms_of_use_sv=obj["terms_of_use_sv"],
            terms_of_use_en=obj["terms_of_use_en"],
        )
        if save:
            instance.save()
        pk_map[obj["pk"]] = instance.pk
    return pk_map


def _import_resources(data: dict, save: bool = False) -> dict:
    pk_map = {}
    for obj in data["resources"]:
        # obj:
        # {
        #   "pk": 1,
        #   "name_fi": "Joku esineresurssi",
        #   "name_sv": "N\u00e5gon itemresurs",
        #   "name_en": "Some item resource",
        #   "description_fi": "Suomenkielinen kuvaus",
        #   "description_sv": "Svenska h\u00e4r",
        #   "description_en": "English description",
        #   "is_draft": true,
        #   "location_type": null,
        #   "space": null,
        #   "buffer_time_before": null,
        #   "buffer_time_after": null
        # }
        location_type_map = {
            "fixed": Resource.LOCATION_FIXED,
            "movable": Resource.LOCATION_MOVABLE,
        }
        instance = Resource(
            name=obj["name_fi"],
            name_fi=obj["name_fi"],
            name_sv=obj["name_sv"],
            name_en=obj["name_en"],
            description=obj["description_fi"],
            description_fi=obj["description_fi"],
            description_sv=obj["description_sv"],
            description_en=obj["description_en"],
            is_draft=obj["is_draft"],
            location_type=location_type_map[obj["location_type"]],
            space_id=obj["space"],
            buffer_time_before=obj["buffer_time_before"],
            buffer_time_after=obj["buffer_time_after"],
        )
        if save:
            instance.save()
        pk_map[obj["pk"]] = instance.pk
    return pk_map


# No dependencies
def _import_purposes(data: dict, save: bool = False) -> dict:
    pk_map = {}
    for obj in data["purposes"]:
        # obj:
        # {
        #   "pk": 1,
        #   "name_fi": "Joku k\u00e4ytt\u00f6tarkoitus",
        #   "name_sv": "N\u00e5got purpose",
        #   "name_en": "Some purpose"
        # }
        instance = Purpose(
            name=obj["name_fi"],
            name_fi=obj["name_fi"],
            name_sv=obj["name_sv"],
            name_en=obj["name_en"],
        )
        if save:
            instance.save()
        pk_map[obj["pk"]] = instance.pk
    return pk_map


# No dependencies
def _import_units(data: dict, save: bool = False) -> dict:
    pk_map = {}
    for obj in data["units"]:
        # obj:
        # {
        #   "pk": 1,
        #   "tprek_id": "axg26o4luvta",
        #   "name_fi": "Joku toimipiste",
        #   "name_sv": "N\u00e5gon enhet",
        #   "name_en": "Some unit",
        #   "description_fi": "Joku kuvaus",
        #   "description_sv": "N\u00e5gon description",
        #   "description_en": "Some description",
        #   "web_page": null,
        #   "email": "manageri@example.com",
        #   "phone": null,
        #   "short_description_fi": null,
        #   "short_description_sv": null,
        #   "short_description_en": null
        # }
        instance = Unit(
            tprek_id=obj["tprek_id"],
            name=obj["name_fi"],
            name_fi=obj["name_fi"],
            name_sv=obj["name_sv"],
            name_en=obj["name_en"],
            description=obj["description_fi"],
            description_fi=obj["description_fi"],
            description_sv=obj["description_sv"],
            description_en=obj["description_en"],
            web_page=obj["web_page"] if obj["web_page"] is not None else "",
            email=obj["email"],
            phone=obj["phone"] if obj["phone"] is not None else "",
            short_description=obj["short_description_fi"] or "",
            short_description_fi=obj["short_description_fi"] or "",
            short_description_sv=obj["short_description_sv"] or "",
            short_description_en=obj["short_description_en"] or "",
        )
        if save:
            instance.save()
        pk_map[obj["pk"]] = instance.pk
    return pk_map


# No dependencies
def _import_reservation_unit_types(data: dict, save: bool = False) -> dict:
    pk_map = {}
    for obj in data["reservation_unit_types"]:
        # obj:
        # {
        #   "pk": 1,
        #   "name_fi": "Joku esine",
        #   "name_sv": "F\u00f6rem\u00e5l",
        #   "name_en": "Some item"
        # }
        instance = ReservationUnitType(
            name=obj["name_fi"],
            name_fi=obj["name_fi"],
            name_sv=obj["name_sv"],
            name_en=obj["name_en"],
        )
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
    for obj in data["reservation_units"]:
        # obj:
        # {
        #   "pk": 1,
        #   "name_fi": "Joku esineresurssi",
        #   "name_sv": "N\u00e5gon itemresurs",
        #   "name_en": "Some item resource",
        #   "description_fi": "Suomenkielinen kuvaus",
        #   "description_sv": "Svenska h\u00e4r",
        #   "description_en": "English description",
        #   "reservation_unit_type_id": 1,
        #   "unit_id": 1,
        #   "contact_information_fi": "Yhteyshenkil\u00f6n tiedot",
        #   "contact_information_sv": "Information av kontaktpersonen",
        #   "contact_information_en": "Contact person details",
        #   "is_draft": false,
        #   "max_persons": 15,
        #   "surface_area": 2,
        #   "keyword_groups": null,
        #   "services": null,
        #   "require_introduction": null,
        #   "terms_of_use_fi": null,
        #   "terms_of_use_sv": null,
        #   "terms_of_use_en": null,
        #   "max_reservation_duration": null,
        #   "min_reservation_duration": null,
        #   "buffer_time_between_reservations": null,
        #   "resources": "1",
        #   "spaces": null,
        #   "purposes": "1",
        #   "equipments": "1"
        # }
        instance = ReservationUnit(
            name=obj["name_fi"],
            name_fi=obj["name_fi"],
            name_sv=obj["name_sv"],
            name_en=obj["name_en"],
            description=obj["description_fi"],
            description_fi=obj["description_fi"],
            description_sv=obj["description_sv"],
            description_en=obj["description_en"],
            reservation_unit_type_id=reservation_unit_type_map[
                obj["reservation_unit_type_id"]
            ],
            unit_id=unit_map[obj["unit_id"]],
            contact_information=obj["contact_information_fi"],
            contact_information_fi=obj["contact_information_fi"],
            contact_information_sv=obj["contact_information_sv"],
            contact_information_en=obj["contact_information_en"],
            is_draft=obj["is_draft"],
            max_persons=obj["max_persons"],
            surface_area=obj["surface_area"],
            require_introduction=obj["require_introduction"] or False,
            terms_of_use=obj["terms_of_use_fi"],
            terms_of_use_fi=obj["terms_of_use_fi"],
            terms_of_use_sv=obj["terms_of_use_sv"],
            terms_of_use_en=obj["terms_of_use_en"],
            max_reservation_duration=obj["max_reservation_duration"],
            min_reservation_duration=obj["min_reservation_duration"],
            buffer_time_between_reservations=obj["buffer_time_between_reservations"],
        )
        try:
            spaces = [space_map[int(obj["pk"].strip())]]
        except AttributeError:
            spaces = []
        try:
            resources = [resource_map[int(obj["pk"].strip())]]
        except AttributeError:
            resources = []
        if obj["purposes"]:
            purposes = [
                purpose_map[int(pk.strip())] for pk in obj["purposes"].split(",")
            ]
        else:
            purposes = []
        if obj["equipments"]:
            equipments = [
                equipment_map[int(pk.strip())] for pk in obj["equipments"].split(",")
            ]
        else:
            equipments = []
        if save:
            instance.save()
            instance.resources.set(resources)
            instance.spaces.set(spaces)
            instance.purposes.set(purposes)
            instance.equipments.set(equipments)
        pk_map[obj["pk"]] = instance.pk
    return pk_map


# No dependencies
def _import_equipment_categories(data: dict, save: bool = False) -> dict:
    pk_map = {}
    for obj in data["equipment_categories"]:
        # obj:
        # {
        #   "pk": 1,
        #   "name_fi": "Joku varustekategoria",
        #   "name_sv": "N\u00e5gon equipmentkategori",
        #   "name_en": "Some equipment category"
        # }
        instance = EquipmentCategory(
            name=obj["name_fi"],
            name_fi=obj["name_fi"],
            name_sv=obj["name_sv"],
            name_en=obj["name_en"],
        )
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
        # obj:
        # {
        #   "pk": 1,
        #   "name_fi": "Joku varuste",
        #   "name_sv": null,
        #   "name_en": "Some equipment",
        #   "category_id": 1
        # }
        instance = Equipment(
            name=obj["name_fi"],
            name_fi=obj["name_fi"],
            name_sv=obj["name_sv"],
            name_en=obj["name_en"],
            category_id=equipment_category_map[obj["category_id"]],
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

    _ = _import_reservation_units(
        json_data,
        space_map,
        resource_map,
        purpose_map,
        reservation_unit_type_map,
        equipment_map,
        unit_map,
        save,
    )
