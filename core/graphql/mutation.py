import inspect

import graphene
from django.core.exceptions import ValidationError
from django.db import transaction
from stringcase import snakecase

from core.graphql.exception import ErrorMessage, MutationException
from core.graphql.helper import from_global_id
from core.django.models import ArchiveModel


# ==================================================================================================== Base Mutation
class BaseMutationMixin(object):
    id_name = 'id'
    model = None

    status = graphene.Int()
    errors = graphene.List(ErrorMessage)

    @classmethod
    def get_primary_input_name(cls):
        return snakecase(cls.model.__name__)

    @classmethod
    def get_node_name(cls):
        return f'{cls.model.__name__}Node'

    @classmethod
    def parse_global_id(cls):
        """base64 global id to int id"""
        return f'{cls.model.__name__}Node'

    @classmethod
    def get_input_fields(cls):
        return (x for x in cls.Input._meta.fields)

    @staticmethod
    def id_required_mutation(func):
        """Decorator for graphql mutation class,usage:
            @Authenticator.id_required_mutation
            def mutate_and_get_payload(cls, root, info, **input):
        """

        def wrapper_id_required(cls, root, info, **inputs):
            if not inputs.get(cls.id_name, '').strip():
                return cls(status=400, errors={'mandatory': ['Please provide id.']})
            return func(cls, root, info, **inputs)

        return wrapper_id_required

    @staticmethod
    def login_required_mutation(func):
        """Decorator for graphql mutation class,usage:
            @Authenticator.login_required_mutation
            def mutate_and_get_payload(cls, root, info, **input):
        """

        def wrapper_login_required(cls, root, info, **inputs):
            if not info.context.user.is_authenticated:
                return cls(status=403)
            return func(cls, root, info, **inputs)

        return wrapper_login_required

    def role_required_mutation(func):
        # todo
        raise NotImplementedError

    @classmethod
    def validate_fk_field(cls, data, field_name, fk_model, mandatory=True):
        """convert base64 global id to local db id"""
        base64_id = data.get(field_name, None)

        if not base64_id and mandatory:
            raise MutationException(f'Please provide `{field_name}`.', code='mandatory')

        try:
            _type, db_id = from_global_id(base64_id)
        except Exception as ex:
            raise MutationException(f'Please provide a validate global id for field {field_name}.', code='not_found')

        if fk_model.objects.filter(id=db_id).exists():
            data[field_name] = db_id  # replace base64 global id with db int id
        else:
            raise MutationException(f'{field_name} id={base64_id} not found.', code='not_found')

    @classmethod
    def validate(cls, root, info, **inputs):
        """check the inputs is validated or not"""
        return inputs

    @classmethod
    def process(cls, root, info, **inputs):
        """do the actual business logic"""
        raise NotImplementedError

    @classmethod
    def response(cls, root, info, result, **inputs):
        """return the response"""
        return cls(status=200)

    @classmethod
    def process_related(cls, root, info, result, **inputs):
        pass

    @classmethod
    def mutate_and_get_payload(cls, root, info, **inputs):
        try:
            with transaction.atomic():
                inputs = cls.validate(root, info, **inputs)
                result = cls.process(root, info, **inputs)
                cls.process_related(root, info, result, **inputs)
                return cls.response(root, info, result, **inputs)
        except (MutationException, ValidationError) as ex:
            return cls(status=400, errors=[ErrorMessage(code=ex.code, message=ex.message)])
        except Exception as ex:
            return cls(status=500, errors=[ErrorMessage(code=ex.__class__.__name__, message=str(ex))])


class CreateMutationMixin(BaseMutationMixin):
    @classmethod
    def validate(cls, root, info, **inputs):
        if cls.model:
            input_name = cls.get_primary_input_name()
            if inputs.get(input_name, {}):
                return inputs
            else:
                raise MutationException(f'Please provide data for {input_name}', code='mandatory')

        raise NotImplementedError

    @classmethod
    def create_related(cls, parent_obj, fk_model, fk_field_name, input_name, **inputs):
        kwargs = inputs.get(input_name, {})
        if kwargs and fk_field_name and parent_obj:
            data = {**{fk_field_name: parent_obj.id}, **kwargs}
            if data:
                return fk_model.objects.create(**data)
        return None

    @classmethod
    def get_create_from_model(cls):
        """check model have classmethod create() or not"""
        create_func = getattr(cls.model, 'create', None)
        if inspect.ismethod(create_func):
            return create_func
        return None

    @classmethod
    def process(cls, root, info, **inputs):
        if cls.model:
            input_name = cls.get_primary_input_name()
            data = inputs.get(input_name, {})
            if not data:
                raise MutationException(f'Please provide data for {input_name}', code='mandatory')
            try:
                # try to use create classmethod in model
                create_func = cls.get_create_from_model()
                if create_func:
                    obj = create_func(**data)
                else:
                    obj = cls.model.objects.create(**data)
            except Exception as ex:
                raise MutationException(str(ex), code=ex.__class__.__name__)

            return obj
        raise NotImplementedError

    @classmethod
    def response(cls, root, info, result, **inputs):
        if cls.model:
            resp = cls(status=200)
            input_name = cls.get_primary_input_name()
            setattr(resp, input_name, result)
            return resp
        raise NotImplementedError


class UpdateMutationMixin(BaseMutationMixin):
    @classmethod
    def validate(cls, root, info, **inputs):
        base64_id = inputs.get(cls.id_name, '').strip()
        if not base64_id:
            raise MutationException('Please provide id.', code='mandatory')

        _type, _id = from_global_id(base64_id)
        if not cls.model.objects.filter(id=_id).exists():
            raise MutationException(f'{cls.model.__name__} id={base64_id} not found.', code='not_found')

        return inputs

    @classmethod
    def process(cls, root, info, **inputs):
        if cls.model:
            base64_id = inputs.get(cls.id_name, '').strip()
            input_name = cls.get_primary_input_name()
            input_data = inputs.get(input_name, {})
            if base64_id and input_data:
                _type, _id = from_global_id(base64_id)
                updated_count = cls.model.objects.filter(id=_id).update(**input_data)
                if not updated_count:
                    raise MutationException(f'{input_name} with id={_id} not found.', code='not_found')

                obj = cls.model.objects.get(id=_id)
                return obj
            raise MutationException(f'{input_name} with id={base64_id} not found.', code='not_found')
        raise NotImplementedError

    @classmethod
    def response(cls, root, info, result, **inputs):
        if cls.model:
            input_name = cls.get_primary_input_name()

            data = {"status": 200, input_name: result}
            resp = cls(**data)
            return resp
        raise NotImplementedError


class DeleteMutationMixin(BaseMutationMixin):
    @classmethod
    def validate(cls, root, info, **inputs):
        if not inputs.get(cls.id_name, '').strip():
            raise MutationException(f'Please provide id for {cls.model.__name__}.', code='mandatory')
        return inputs

    @classmethod
    def process(cls, root, info, **inputs):
        """delete object according id, if it's from ArchiveModel then just archive it"""
        if cls.model:
            base64_id = inputs.get(cls.id_name, '').strip()
            if base64_id:
                _type, _id = from_global_id(base64_id)
                if not _type.startswith(cls.model.__name__):
                    # base64 id type not match
                    raise MutationException(f'{base64_id} is a invalid {cls.model.__name__} id.', code='not_found')

                if issubclass(cls.model, ArchiveModel):
                    delete_count = cls.model.objects.filter(id=_id).update(is_archived=True)
                    # deleted_object = delete_count and cls.model.objects.get(id=_id) or None
                    deleted_object = None  # at this moment only return 200 status without deleted object
                else:
                    delete_count, deleted_object = cls.model.objects.filter(id=_id).delete()

                if not delete_count:
                    raise MutationException(f'{cls.model.__name__} with id={_id} not found.',
                                            code='not_found')
                return deleted_object
            else:
                raise MutationException(f'Please provide id for {cls.model.__name__}',
                                        code='mandatory')
        raise NotImplementedError
