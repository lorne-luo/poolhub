from django.db import models
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from model_utils.managers import InheritanceManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class ArchiveQuerySet(models.QuerySet):

    def filter(self, *args, **kwargs):
        fields = list(filter(lambda x: x.startswith(ArchiveModel.archive_field_name), kwargs.keys()))

        if not fields:
            kwargs[ArchiveModel.archive_field_name] = False
        return super(ArchiveQuerySet, self).filter(*args, **kwargs)


class ArchiveModelManager(models.Manager):
    def non_archives(self):
        return super().filter(is_archived=False)

    def archives(self):
        return super().filter(is_archived=True)



class InheritanceArchiveManager(ArchiveModelManager, InheritanceManager):
    pass

class ArchiveModel(BaseModel):
    """abstract archiveable model"""
    archive_field_name = 'is_archived'
    is_archived = models.BooleanField(blank=True, default=False)

    objects = ArchiveModelManager()

    class Meta:
        abstract = True

    @property
    def not_archived(self):
        return not self.is_archived


class NameSlugModel(models.Model):
    slug = AutoSlugField(populate_from='name', blank=True)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        super(NameSlugModel, self).save(force_insert, force_update, using, update_fields)
