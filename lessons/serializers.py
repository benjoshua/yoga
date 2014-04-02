from rest_framework import serializers

from lessons.models import User, Lesson


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'lessons', )


class LessonSerializer(serializers.ModelSerializer):
    lessonType = serializers.SlugRelatedField(slug_field='name')
    location = serializers.SlugRelatedField(slug_field='name')
    has_room = serializers.Field(source='spots_left')
    #last_registered = serializers.Field(source='last_registered')

    class Meta:
        model = Lesson
        fields = ('id','lessonType','date','location','length', 'has_room')

class LessonDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
