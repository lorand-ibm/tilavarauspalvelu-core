import hashlib
import hmac
import urllib.parse

def gen():
    secret_key = (
        "31fba70bc32005b914b5c488f0c037ad0d59a90b"
    )


    get_parameters_string = "hsa_source=tvp&hsa_username=tvp&hsa_organization=tprek%3Acfe4d81b-7366-4ae2-b87b-b986e10cd220&hsa_resource=tvp%3A1f0634ad-a991-43b2-8ea6-371ae8f6a97e&hsa_created_at=2021-05-04T10%3A35%3A00.917Z&hsa_valid_until=2021-05-04T16%3A45%3A00.917Z&hsa_signature=17aecfbf3c98bb59f29f185a196cf70d3e0aced2afcac20c948aa47e5dad3ef1"

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

    payload_signature = payload["hsa_signature"]

    calculated_signature = hmac.new(
    key=secret_key.encode("utf-8"),
    msg=data_string.encode("utf-8"),
    digestmod=hashlib.sha256,
    ).hexdigest()

    print("Payload sig   : ", payload_signature)
    print("Calculated sig: ", calculated_signature)

    if hmac.compare_digest(payload_signature, calculated_signature):
        print("Payload ok")
    else:
        print("Invalid payload")