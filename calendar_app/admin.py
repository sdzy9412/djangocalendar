# Register your models here.
from django.contrib import admin
from calendar_app.models import Event, EventMember

class EventMemberAdmin(admin.ModelAdmin):
    model = EventMember
    list_display = ['event', 'user']

admin.site.register(Event)
admin.site.register(EventMember, EventMemberAdmin)
