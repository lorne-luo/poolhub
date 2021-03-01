import django_filters
from graphql_relay import to_global_id
from graphql_relay.utils import unbase64

from core.django.models import ArchiveModel


def from_global_id(global_id):
    """return a db int id"""
    if isinstance(global_id, int) or global_id.isdigit():
        return global_id

    unbased_global_id = unbase64(global_id)
    _type, _id = unbased_global_id.split(':', 1)
    return _type, _id
