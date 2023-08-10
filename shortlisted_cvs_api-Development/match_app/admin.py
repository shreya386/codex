from django.contrib import admin


# Register your models here.
from .models import (
    JobDetail,
    WorkerAttachment,
    ExperienceLevelMaster,
    JobTitleMaster,
    UserMaster,
)


# # # # Register your models here.
admin.site.register(JobDetail)
admin.site.register(WorkerAttachment)
admin.site.register(ExperienceLevelMaster)
admin.site.register(JobTitleMaster)
admin.site.register(UserMaster)
