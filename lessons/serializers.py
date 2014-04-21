from rest_framework import serializers

from lessons.models import User, Lesson, RegisteredStudent


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'lessons', )


class RegisteredStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegisteredStudent

class LessonSerializer(serializers.ModelSerializer):
    lessonType = serializers.SlugRelatedField(slug_field='name')
    location = serializers.SlugRelatedField(slug_field='name')
    has_room = serializers.Field(source='spots_left')
    last_registered = serializers.Field(source='last_registered')

    class Meta:
        model = Lesson
        fields = ('id','lessonType','date','location','length', 'has_room', 'students', 'last_registered')

class LessonDetailSerializer(serializers.ModelSerializer):
    #students = RegisteredStudentSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ('id','lessonType','date','location','length')
