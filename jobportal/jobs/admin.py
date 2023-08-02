from django.contrib import admin
from candidates.models import CandidateJobMap
from .models import jobs


class CandidateInline(admin.TabularInline):
    model = CandidateJobMap
    def get_readonly_fields(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return []
        else:
            return ('candidate',)    

class JobAdmin(admin.ModelAdmin):
    exclude = ('creater',)
    list_display = ('Position_name','creater',)
    inlines = (CandidateInline, )
    def get_queryset(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return jobs.objects.all()
        else:
            return jobs.objects.filter(creater=request.user )

    def get_list_display(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return ('Position_name','creater',)
        else:
            return ('Position_name',)
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creater = request.user
            obj.save()


admin.site.register(jobs, JobAdmin)
