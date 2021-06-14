from django.contrib import admin
from django import forms

# Register your models here.
from apps.tenant.models import Domain, Tenant


class DomainAdminForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = '__all__'


class DomainAdmin(admin.ModelAdmin):
    form = DomainAdminForm
    list_display = ['domain', 'tenant', 'is_primary']


admin.site.register(Domain, DomainAdmin)

class TenantAdminForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = '__all__'


class TenantAdmin(admin.ModelAdmin):
    form = TenantAdminForm
    list_display = ['name', 'schema_name']


admin.site.register(Tenant, TenantAdmin)
