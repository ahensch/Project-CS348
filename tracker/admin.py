from django.contrib import admin
from .models import Member, Event, HourLog, SemesterRequirement

admin.site.register(Member)
admin.site.register(Event)
admin.site.register(HourLog)
admin.site.register(SemesterRequirement)
