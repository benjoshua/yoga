from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Lesson(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField('Lesson Time')
    def current_time(self):
        return timezone.now()
    
    def spots_left(self):
        return 15
    
    def __unicode__(self):
        return self.name

class StudentsClassTime(models.Model):
    student = models.ForeignKey(User)
    lesson = models.ForeignKey(Lesson)
    def __unicode__(self):
        return unicode(self.student) + ', ' + unicode(self.lesson)