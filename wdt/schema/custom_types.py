from datetime import datetime

from ariadne import ScalarType
from dateutil.parser import isoparse
from django.utils.timezone import make_aware, utc


datetime_scalar = ScalarType("DateTime")


@datetime_scalar.serializer
def serialize_datetime(value: datetime):
    iso_datetime = value.isoformat(timespec="milliseconds")

    if iso_datetime.endswith("+00:00"):
        return f"{iso_datetime[:-6]}Z"

    return iso_datetime


@datetime_scalar.value_parser
def parse_datetime(value):
    parsed_datetime = isoparse(value)

    if parsed_datetime.tzinfo:
        return parsed_datetime

    return make_aware(parsed_datetime, utc)
