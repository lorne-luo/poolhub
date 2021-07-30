from django.db import models

from django_tenants.models import DomainMixin, TenantMixin
from django.db import models, connection


class Domain(DomainMixin):
    pass

    def __str__(self):
        return self.domain

class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField(null=True)
    on_trial = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.schema_name

    def set_schema(self):
        schema_name = self.schema_name
        if schema_name:
            connection.set_schema(schema_name)
