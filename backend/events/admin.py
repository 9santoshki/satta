# betting/admin.py
from django.contrib import admin
from .models import Event, Outcome, Bet

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


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'outcome', 'amount', 'is_won', 'created_at')
    list_filter = ('user', 'event', 'outcome', 'is_won')
    search_fields = ('user__username', 'event__title', 'outcome__title')
