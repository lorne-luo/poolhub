import graphene
from django.core.exceptions import ValidationError


class ErrorMessage(graphene.ObjectType):
    code = graphene.String()
    message = graphene.String()


class MutationException(ValidationError):
    pass
