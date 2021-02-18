# Api
# Api layer to handle calling AllocationData constructor with proper data and call the solver
class AllocationRequest():
    application_round_id = int
    reservation_unit_ids = Optional[List[int]]
    application_round_basket_ids = Optional[[int]]



class ApplicationEventSchedule(models.Model):
    VALIDATED = "validated"
    DECLINED = "declined"
    CANCELLED = "cancelled"
    HANDLED = "handled"

    STATUS_CHOICES = (
        (VALIDATED, _("Validated")),
        (DECLINED, _("Declined")),
        (CANCELLED, _("Cancelled")),
        (HANDLED, _("Handled")),
    )

    status = models.CharField(
        max_length=20, verbose_name=_("Status"), choices=STATUS_CHOICES
    )

# Response
# Multi table inheritance
class ApplicationEventScheduleResult(ApplicationEventSchedule):
    allocated_duration = models.DurationField()
    day = models.IntegerField(verbose_name=_("Day"), choices=DATE_CHOISES, null=False)

    begin = models.TimeField(
        verbose_name=_("Start"),
        null=False,
        blank=False,
    )

    end = models.TimeField(
        verbose_name=_("End"),
        null=False,
        blank=False,
    )

    application_event = models.ForeignKey(
        ApplicationEventResult,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="application_event_schedules",
    )
    recurrence = models.RecurrenceField(
        begin,
        end,
        exdates=[]
    )


# The base application event model
class ApplicationEvent(models.Model):
    print("not abstract")
# Response
# Multi table inheritance
class ApplicationEventResult(ApplicationEvent):
    num_allocated_events_per_week = models.PositiveIntegerField()
    events = ApplicationEventScheduleResult

class Reservation():
    print("needs link to application event")
