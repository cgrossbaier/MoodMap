from django.contrib import admin
from django.db import models
from .models import Event

class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['user']}),
        ('Date information', {'fields': ['creation_date', 'valid_until']}),
        ('Event information', {'fields': ['eventType', 'lng', 'lat']}),
    ]
    list_display = ('user', 'creation_date')
    list_filter = ['creation_date']
    search_fields = ['user']
    
admin.site.register(Event, EventAdmin)