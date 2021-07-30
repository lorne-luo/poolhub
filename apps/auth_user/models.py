from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.constants import UserRole


class User(AbstractUser):
    """user for authentication"""
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    email = models.EmailField(_('email address'), blank=False, null=False, unique=True)
    phone_number = models.CharField(_('phone number'), max_length=16, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    role = models.CharField(verbose_name="user role", choices=UserRole.CHOICES, max_length=32, blank=True,
                            null=False)
    tenant = models.ForeignKey('tenant.Tenant', blank=True, null=True, on_delete=models.SET_NULL)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
