import django_filters
import graphene
from graphql_relay import to_global_id

from core.django.models import ArchiveModel


class CountableNodeConnection(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()
    edge_count = graphene.Int()

    def resolve_total_count(root, info, **kwargs):
        return root.length

    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)


class PhotoModelNodeMixin(object):
    photo = graphene.String()

    def resolve_photo(parent, info):
        return parent.photo_url


class ArchiveModelFilter(django_filters.FilterSet):
    def filter_queryset(self, queryset):
        queryset = super(ArchiveModelFilter, self).filter_queryset(queryset)
        if issubclass(self._meta.model, ArchiveModel):
            fields = list(filter(lambda x: x.startswith(ArchiveModel.archive_field_name),
                                 self.form.cleaned_data.keys()))
            is_archive_conditions = list(filter(lambda x: self.form.cleaned_data.get(x) in [True, False], fields))
            if not is_archive_conditions:
                queryset = queryset.filter(is_archived=False)
        return queryset


class NodeModelMixin(object):
    """used for django model to get global base64 id"""

    @property
    def global_id(self):
        if not self.id:
            return None
        # regulation: { model name}Node
        return to_global_id(f'{self.__class__.__name__}Node', self.id)
