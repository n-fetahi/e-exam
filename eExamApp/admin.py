from django.contrib import admin
from eExamApp import models

# Register your models here.

admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.College)
admin.site.register(models.Specialization)
admin.site.register(models.Level)
admin.site.register(models.Exam_Models)

