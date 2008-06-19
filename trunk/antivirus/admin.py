# Admin registrations
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from models import File

class FileAdmin(ModelAdmin):
    list_display = ('path','status',)
    list_filter = ('status',)
    search_fields = ('path',)

admin.site.register(File, FileAdmin)

