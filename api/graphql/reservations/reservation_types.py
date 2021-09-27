import graphene
from graphene_permissions.mixins import AuthNode
from graphql.execution.base import ResolveInfo
from rest_framework.reverse import reverse

from api.graphql.base_type import PrimaryKeyObjectType
from api.ical_api import hmac_signature
from reservations.models import Reservation


class ReservationType(AuthNode, PrimaryKeyObjectType):
    class Meta:
        model = Reservation

        interfaces = (graphene.relay.Node,)

    calendar_url = graphene.String()

    def resolve_calendar_url(self, info: ResolveInfo) -> str:
        if self is None:
            return ""
        scheme = info.context.scheme
        host = info.context.get_host()
        calendar_url = reverse("reservation_calendar-detail", kwargs={"pk": self.pk})
        signature = hmac_signature(f"reservation-{self.pk}")
        return f"{scheme}://{host}{calendar_url}?hash={signature}"
