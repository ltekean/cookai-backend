from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_gt0(value):
    if value <= 0:
        raise ValidationError(
            _(f"{value}는 0 보다 작거나 같습니다."),
            params={"value": value},
        )
