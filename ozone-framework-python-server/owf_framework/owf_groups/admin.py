from django.contrib import admin
from owf_framework.stacks.admin import StackGroupInline
from .models import OWFGroup


class OWFGroupPeopleInline(admin.TabularInline):
    model = OWFGroup.people.through


class OWFGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_name', 'name', 'status', 'description')
    search_fields = ('display_name', 'name',)
    verbose_name = 'OWF Group'
    verbose_name_plural = 'OWF Groups'
    inlines = [OWFGroupPeopleInline, StackGroupInline, ]
    exclude = ('person',)


admin.site.register(OWFGroup, OWFGroupAdmin)