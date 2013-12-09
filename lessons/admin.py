from django.contrib import admin
from lessons.models import Lesson, StudentsClassTime

class LessonAdmin(admin.ModelAdmin):
    list_display = ('name','date')


admin.site.register(Lesson, LessonAdmin)
admin.site.register(StudentsClassTime)

# Register your models here.
