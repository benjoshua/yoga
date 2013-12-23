from django.contrib import admin
from lessons.models import Lesson

class LessonAdmin(admin.ModelAdmin):
    list_display = ('name','date','student_list')


admin.site.register(Lesson, LessonAdmin)

# Register your models here.
