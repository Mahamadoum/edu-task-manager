from django.contrib import admin
from .models import Discipline


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active')
