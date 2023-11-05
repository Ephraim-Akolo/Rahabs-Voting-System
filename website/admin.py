from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.User)
admin.site.register(models.PoliticalParty)
admin.site.register(models.Election)
admin.site.register(models.State)
admin.site.register(models.LocalGorvernment)
admin.site.register(models.Candidate)
