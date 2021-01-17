from django.contrib import admin

from .models import Place, Review

class PlaceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['name']}),
        ('Address', {'fields': ['street_address', 'suburb', 'state','postcode']}),
    ]

admin.site.register(Place, PlaceAdmin)
admin.site.register(Review)
