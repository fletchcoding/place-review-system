from django.contrib import admin

from .models import Place, Review, Feedback, Scorecard

class FeedbackInline(admin.StackedInline):
    model = Feedback

class ScorecardInline(admin.TabularInline):
    model = Scorecard

class PlaceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['name']}),
        ('Address', {'fields': ['street_address', 'suburb', 'state','postcode']}),
    ]
    inlines = [ScorecardInline]

class ReviewAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Date & Time', {'fields': ['visit_date']}),
        ('Place', {'fields': ['place']}),
        ('User', {'fields': ['reviewer']}),
    ]
    inlines =  [FeedbackInline]

admin.site.register(Place, PlaceAdmin)
admin.site.register(Review, ReviewAdmin)
