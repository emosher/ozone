from django.db import models
from owf_groups.models import OwfGroup
from people.models import Person


class Stack(models.Model):
    id = models.BigAutoField(primary_key=True)
    version = models.BigIntegerField()
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=4000, blank=True, null=True)
    stack_context = models.CharField(unique=True, max_length=200)
    image_url = models.CharField(max_length=2083, blank=True, null=True)
    descriptor_url = models.CharField(max_length=2083, blank=True, null=True)
    unique_widget_count = models.BigIntegerField(blank=True, null=True)
    owner = models.ForeignKey(Person, models.DO_NOTHING, blank=True, null=True)
    approved = models.BooleanField(blank=True, null=True)
    default_group = models.ForeignKey(OwfGroup, models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'stack'


class StackGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(OwfGroup, models.DO_NOTHING)
    stack = models.ForeignKey(Stack, models.DO_NOTHING)

    def __str__(self):
        return f'{self.group.name} for stack name {self.stack.name}'

    class Meta:
        managed = True
        db_table = 'stack_groups'
        unique_together = (('group', 'stack'),)