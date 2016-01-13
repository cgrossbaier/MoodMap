from django.contrib import admin
from django.db import models
from .models import Event, Statistic, Feedback

class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['user']}),
        ('Date information', {'fields': ['creation_date', 'valid_until']}),
        ('Event information', {'fields': ['eventType', 'lng', 'lat']}),
    ]
    list_display = ('user', 'eventType', 'creation_date')
    list_filter = ['creation_date']
    search_fields = ['user']

admin.site.register(Event, EventAdmin)

class StatisticAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['user']}),
        ('Date information', {'fields': ['timestamp']}),
        ('Event information', {'fields': ['statType', 'lng', 'lat', 'zoom']}),
    ]
    list_display = ('user', 'timestamp')
    list_filter = ['timestamp']
    search_fields = ['user']
    
admin.site.register(Statistic, StatisticAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['user']}),
        ('Feedback', {'fields': ['feedback1', 'feedback2', 'feedback3']}),
    ]

admin.site.register(Feedback, FeedbackAdmin)

