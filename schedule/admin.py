from django.contrib import admin
from .models import Calendar, Display, Event, Location

class CalendarAdmin(admin.ModelAdmin):
    list_display = ('url',)

class DisplayAdmin(admin.ModelAdmin):
    list_display = ('description',)

class EventAdmin(admin.ModelAdmin):
    list_display = ('custom_id', 'calendar', 'start', 'end', 'summary')

# Register your models here.
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Display)
admin.site.register(Event, EventAdmin)
admin.site.register(Location)

