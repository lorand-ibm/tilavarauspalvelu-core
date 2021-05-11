import threading

from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.forms import CharField, ModelForm, forms, URLField
from tinymce.widgets import TinyMCE

from opening_hours.hauki_link_generator import generate_hauki_link
from .models import (
    Day,
    DayPart,
    Equipment,
    EquipmentCategory,
    Period,
    Purpose,
    ReservationUnit,
    ReservationUnitImage,
    ReservationUnitType,
)


class ReservationUnitAdminForm(ModelForm):
    description = CharField(widget=TinyMCE())
    terms_of_use = CharField(widget=TinyMCE())
    extra_stuff = URLField()

    def get_extra_stuff(self):
        return "titties"
    class Meta:
        model = ReservationUnit
        fields = "__all__"


class ReservationUnitImageInline(admin.TabularInline):
    model = ReservationUnitImage


class ModelAdminRequestMixin(object):
    def __init__(self, *args, **kwargs):
        # let's define this so there's no chance of AttributeErrors
        self._request_local = threading.local()
        self._request_local.request = None
        super().__init__(*args, **kwargs)

    def get_request(self):
        return self._request_local.request

    def set_request(self, request):
        self._request_local.request = request

    def changeform_view(self, request, *args, **kwargs):
        # stash the request
        self.set_request(request)

        # call the parent view method with all the original args
        return super().changeform_view(request, *args, **kwargs)

    def add_view(self, request, *args, **kwargs):
        self.set_request(request)
        return super().add_view(request, *args, **kwargs)

    def change_view(self, request, *args, **kwargs):
        self.set_request(request)
        return super().change_view(request, *args, **kwargs)

    def changelist_view(self, request, *args, **kwargs):
        self.set_request(request)
        return super().changelist_view(request, *args, **kwargs)

    def delete_view(self, request, *args, **kwargs):
        self.set_request(request)
        return super().delete_view(request, *args, **kwargs)

    def history_view(self, request, *args, **kwargs):
        self.set_request(request)
        return super().history_view(request, *args, **kwargs)

@admin.register(ReservationUnit)
class ReservationUnitAdmin(ModelAdminRequestMixin, admin.ModelAdmin):

    model = ReservationUnit
    form = ReservationUnitAdminForm
    inlines = [ReservationUnitImageInline]
    readonly_fields = ["uuid", "fuck_me"]

    def fuck_me(self, a=1, b=2, c=3):
        user = self.get_request().user
        if not user.is_superuser:
            return None
        print("fuck_me")
        return generate_hauki_link(a.uuid, user.email)

    def get_fieldsets(self, request, obj):
        fieldsets = [(None, {'fields': self.get_fields(request, obj)})]
        #fieldsets += ('Extra Fields', {'fields': ('extra_stuff',)})
        fieldsets.append(('Extra Fields', {'fields': ('extra_stuff',)}))
        return fieldsets



@admin.register(ReservationUnitImage)
class ReservationUnitImageAdmin(admin.ModelAdmin):
    model = ReservationUnitImage


@admin.register(ReservationUnitType)
class ReservationUnitTypeAdmin(admin.ModelAdmin):
    model = ReservationUnitType


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    model = Period


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    model = Day


@admin.register(DayPart)
class DayPartAdmin(admin.ModelAdmin):
    model = DayPart


@admin.register(Purpose)
class PurposeAdmin(admin.ModelAdmin):
    model = Purpose
    fields = ["name"]


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    model = Equipment


@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    model = EquipmentCategory
