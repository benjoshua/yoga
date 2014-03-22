from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Teacher(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    email = models.EmailField()
    #picture = models.ImageField()

    def __unicode__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    geoLocationLat = models.FloatField()
    geoLocationLng = models.FloatField()
    capacity = models.IntegerField()
    def __unicode__(self):
        return self.name + ', ' + self.address

class Subscription(models.Model):
    type = models.CharField('Subscription Type', max_length=50)
    expirationDate = models.DateField('Subscription expiration date')
    lessonsLeft = models.IntegerField('Lessons left',default=-1)
    owner = models.OneToOneField(User,primary_key=True)
    def __unicode__(self):
        return self.type + ' expires at ' + str(self.expirationDate)

class LessonType(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=400)
    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    lessonType = models.ForeignKey(LessonType)
    date = models.DateTimeField('Lesson Time')
    teacher = models.ForeignKey(Teacher)
    location = models.ForeignKey(Location)
    length = models.TimeField('Lesson Length', default="01:15")
    notificationList = models.CommaSeparatedIntegerField(blank=True, null=True, max_length=30)
    comments = models.CharField(blank=True, null=True, max_length=200)
    students = models.ManyToManyField(User, through='RegisteredStudent')

    def student_list(self):
        return ", ".join([student.first_name for student in self.students.all()])
    student_list.short_description = "Students"
    
    def current_time(self):
        return timezone.now()
    
    def spots_left(self):
        return self.location.capacity - self.students.count()
    
    def __unicode__(self):
        return self.lessonType.name

class RegisteredStudent(models.Model):
    lesson = models.ForeignKey(Lesson)
    student = models.ForeignKey(User)
    registrationTime = models.DateTimeField()
    attended = models.BooleanField(default=False)











