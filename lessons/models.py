from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Lesson(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    spots = models.IntegerField(default=15)
    date = models.DateTimeField('Lesson Time')
    students = models.ManyToManyField(User, null=True, blank=True)

    def student_list(self):
        return ", ".join([student.first_name for student in self.students.all()])
    student_list.short_description = "Students"
    
    def student_array(self):
        return self.students.all()
    
    def current_time(self):
        return timezone.now()
    
    def spots_left(self):
        return self.spots - self.students.count()
    
    def __unicode__(self):
        return self.name
