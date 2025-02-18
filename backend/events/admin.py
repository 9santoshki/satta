# not using admin

from django.contrib import admin
from .models import Event, Outcome

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('title', 'description')
    date_hierarchy = 'start_time'

@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    list_display = ('event', 'title', 'odds', 'created_at')
    list_filter = ('event',)
    search_fields = ('title',)
