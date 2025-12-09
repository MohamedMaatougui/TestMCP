from django.contrib import admin
from .models import *
# Register your models here.


class SubmissionInLine(admin.TabularInline):
    model = Submission
    extra = 1
    fields = ('title', 'author', 'status', 'payed')


class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'start_date', 'end_date')
    search_fields = ('name', 'location', 'theme')
    list_filter = ('theme', 'start_date', 'end_date', 'location')
    list_per_page = 1
    inlines = [SubmissionInLine]
    readonly_fields = ('conference_id',) 

    #calcul durée
    def duration(self,obj):
        return(obj.end_date - obj.start_date).days
    duration.short_description = "Durée (jours)"

    @admin.action(description="Mark selected submissions as paid")
    def mark_as_paid(modeladmin,request,queryset):
        queryset.update(payed=True)

   
class SubmissionAdmin(admin.ModelAdmin):
    
    list_display = ('submission_id', 'title', 'author', 'conference', 'status', 'submission_date', 'payed')
    list_filter = ('status', 'submission_date', 'payed')
    list_per_page = 1
    
    @admin.action(description="Mark selected submission")
    def mark_as_paid(modeladmin,request,queryset):
        queryset.update(payed=True)
    actions = ['mark_as_paid']


admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(OrganizingCommittee)


admin.site.site_header = "welcome to site"
admin.site.site_title = "training django"
admin.site.index_title = "check this"
