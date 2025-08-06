from django.contrib import admin
from playlist.models import *
# Register your models here.

class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ['id','user','mood']

admin.site.register(MoodEntry,MoodEntryAdmin)