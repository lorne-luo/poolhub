from django.db import connection
from django.urls import set_urlconf, clear_url_caches
from django_tenants.middleware import TenantSubfolderMiddleware
from django_tenants.urlresolvers import get_subfolder_urlconf
from django_tenants.utils import (
    get_public_schema_name,
    get_tenant_model,
    get_subfolder_prefix, get_tenant_domain_model,
)

class CustomTenantMiddleware(TenantSubfolderMiddleware):

    def process_request(self, request):
        # Short circuit if tenant is already set by another middleware.
        # This allows for multiple tenant-resolving middleware chained together.
        if hasattr(request, "tenant"):
            return

        connection.set_schema_to_public()

        urlconf = None

        tenant_model = get_tenant_model()
        domain_model = get_tenant_domain_model()
        hostname = self.hostname_from_request(request)
        subfolder_prefix_path = "/{}/".format(get_subfolder_prefix())

        # We are in the public tenant
        if not request.path.startswith(subfolder_prefix_path):
            try:
                tenant = tenant_model.objects.get(schema_name=get_public_schema_name())
                request.tenant = tenant
            except tenant_model.DoesNotExist:
                raise self.TENANT_NOT_FOUND_EXCEPTION("Unable to find public tenant")

            self.setup_url_routing(request)

        # We are in a specific tenant
        else:
            path_chunks = request.path[len(subfolder_prefix_path):].split("/")
            tenant_subfolder = path_chunks[0]
            try:
                tenant = self.get_tenant(domain_model=domain_model, hostname=tenant_subfolder)
            except domain_model.DoesNotExist:
                return self.no_tenant_found(request, hostname)

            tenant.domain_subfolder = tenant_subfolder
            urlconf = get_subfolder_urlconf(tenant)

        tenant.domain_url = hostname
        request.tenant = tenant

        connection.set_tenant(request.tenant)
        clear_url_caches()  # Required to remove previous tenant prefix from cache, if present

        if urlconf:
            request.urlconf = urlconf
            set_urlconf(urlconf)

