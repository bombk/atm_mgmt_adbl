from django.contrib import admin

from .models import MasterParam


@admin.register(MasterParam)
class MasterParamAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')
    search_fields = ('name', 'value')

# Register your models here.
