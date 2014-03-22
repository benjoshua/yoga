from django.contrib import admin
from lessons.models import Lesson, LessonType, Subscription, RegisteredStudent, Teacher, Location

class LessonAdmin(admin.ModelAdmin):
    list_display = ('lessonType','date','student_list')

class LessonTypeAdmin(admin.ModelAdmin):
    list_display = ('name','description')

class RegisteredStudentAdmin(admin.ModelAdmin):
    list_display = ('lesson','student','registrationTime')


admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonType, LessonTypeAdmin)
admin.site.register(Subscription)
admin.site.register(RegisteredStudent, RegisteredStudentAdmin)
admin.site.register(Teacher)
admin.site.register(Location)

