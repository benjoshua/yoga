from django.db import models
from django.contrib.auth.models import User

class Lesson(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField('Lesson Time')
    def __unicode__(self):
        return self.name

class StudentsClassTime(models.Model):
    student = models.ForeignKey(User)
    lesson = models.ForeignKey(Lesson)
    def __unicode__(self):
        return self.student + ', ' + self.lesson