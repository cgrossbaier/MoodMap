from django.contrib import admin
from django.contrib.gis.db import models
from .models import Choice, Map

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class MapAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['map_title']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ('Map information', {'fields': ['map_center_lat', 'map_center_lon', 'map_center_radius', 'map_center_zoom', 'map_polygon']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('map_title', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['map_title, map_center']

admin.site.register(Map, MapAdmin)