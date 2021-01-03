from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_GUEST = 1
    ROLE_OWNER = 2
    ROLE_CHOICES = (
        (ROLE_GUEST, _('guest')),
        (ROLE_OWNER, _('owner')),
    )

    role = models.PositiveSmallIntegerField(_('role'), choices=ROLE_CHOICES, default=ROLE_GUEST)
    address = models.TextField(_('address'), blank=True)
