from django.contrib import admin
from eExamApp import models

# Register your models here.

admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.College)
admin.site.register(models.Specialization)
admin.site.register(models.Level)
admin.site.register(models.Exam_Models)
admin.site.register(models.Decision)
admin.site.register(models.Decision_And_College)
admin.site.register(models.Decision_And_Level)
admin.site.register(models.Decision_And_Specialization)
admin.site.register(models.Approach)

