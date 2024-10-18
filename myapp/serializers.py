from rest_framework import serializers
from .models import Author, Student, Course, Module, Lesson, Post


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['username', 'password']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'course_image','description', 'duration', 'students_count', 'level', 'lessons_count', 'author', 'rating']

class LessonSerializer(serializers.ModelSerializer):
    module_title = serializers.CharField(source='module.title', read_only=True)
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'video_url', 'short_description', 'content', 'module_title']

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)  # Nested serializer for lessons

    class Meta:
        model = Module
        fields = ['id', 'title', 'lessons']

    def get_course(self, obj):
        return f"{obj.course.title} [id={obj.course.id}]"
