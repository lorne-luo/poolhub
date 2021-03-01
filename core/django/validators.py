import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class NumberOnlyValidator(validators.RegexValidator):
    regex = r'^[0-9]+\Z'
    message = _(
        'Only number accept.'
    )
    flags = 0
