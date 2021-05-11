import hashlib
import hmac
import urllib.parse
from datetime import timedelta
from typing import Union
import datetime
from uuid import UUID

from django.conf import settings


def generate_hauki_link(id: UUID, username: str)-> Union[None, str]:
    if not (settings.HAUKI_API_URL and settings.HAUKI_SECRET and settings.HAUKI_ORIGIN_ID and settings.HAUKI_ORGANISATION_ID):
        return None


    get_parameters_string = f"hsa_source={settings.HAUKI_ORIGIN_ID}&hsa_username=ap.renfors@gmail.com" \
                            f"&hsa_created_at={datetime.datetime.now()}&hsa_valid_until={datetime.datetime.now() + timedelta(minutes=60)}" \
                            f"&hsa_resource={settings.HAUKI_ORIGIN_ID}:{id}"

    payload = dict(urllib.parse.parse_qsl(get_parameters_string))

    data_fields = [
        "hsa_source",
        "hsa_username",
        "hsa_created_at",
        "hsa_valid_until",
        "hsa_organization",
        "hsa_resource",
        "hsa_has_organization_rights",
    ]

    data_string = "".join([payload[field] for field in data_fields if field in payload])

    calculated_signature = hmac.new(
        key=settings.HAUKI_SECRET.encode("utf-8"),
        msg=data_string.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()


    return f"{settings.HAUKI_ADMIN_UI_URL}/resource/{settings.HAUKI_ORIGIN_ID}:{id}/?{get_parameters_string}&hsa_signature={calculated_signature}"
