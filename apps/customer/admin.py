from django.contrib import admin

from django import forms

from apps.customer.models import Customer, Pool


# Register your models here.


class CustomerAdminForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerAdmin(admin.ModelAdmin):
    form = CustomerAdminForm
    list_display = ['first_name', 'last_name', 'email', 'suburb', 'post_code', 'date_joined']
    readonly_fields = ['password', 'date_joined', 'is_superuser']


admin.site.register(Customer, CustomerAdmin)


class PoolAdminForm(forms.ModelForm):
    class Meta:
        model = Pool
        fields = '__all__'


class PoolAdmin(admin.ModelAdmin):
    form = PoolAdminForm
    list_display = ['customer', 'type', 'chlorine_source', 'pool_surface', 'volume']


admin.site.register(Pool, PoolAdmin)
