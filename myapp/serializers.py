from rest_framework import serializers
from .models import Author, Student, Course, Lesson, Post

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'video_url', 'short_description', 'content', 'course']

    def get_course(self, obj):
        return f"{obj.course.course_name} [id={obj.course.id}]"