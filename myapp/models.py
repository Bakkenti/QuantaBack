from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.exceptions import ValidationError
import re

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    about = models.TextField(default="No information available.")
    course_list = models.ManyToManyField('Course', blank=True, related_name='authored_courses')

    def __str__(self):
        return self.username

def validate_course_duration(value):
    # Regex to match the required format for Course duration
    pattern = r'^(?P<value>([1-9]|[1-2][0-9]|30)) (?P<unit>(week|day|weeks|days))$'
    match = re.match(pattern, value)

    if not match:
        raise ValidationError("Write valid duration for course.")

def validate_module_duration(value):
    # Regex to match the required format for Module duration
    pattern = r'^(?P<value>([1-9]|[1-2][0-9]|30)) (?P<unit>(hour|minute|hours|minutes))$'
    match = re.match(pattern, value)

    if not match:
        raise ValidationError("Write valid duration for module.")

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    subscribed_courses = models.ManyToManyField('Course', blank=True)

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    course_image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    description = models.TextField()
    duration = models.CharField(
        max_length=20,
        validators=[validate_course_duration],
        help_text="Enter duration (e.g., '3 weeks' or '1 day')"
    )
    students_count = models.IntegerField(default=0)
    lessons_count = models.IntegerField(default=0)
    level = models.CharField(
        max_length=20,
        choices=[
            ('all', 'All Levels'),
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('expert', 'Expert'),
        ],
        default='all'
    )
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='courses')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.description:
            self.description = self.description.replace('"', '')
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Module(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    duration = models.CharField(
        max_length=20,
        validators=[validate_module_duration],
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')

    def lesson_count(self):
        return self.lessons.count()

    def __str__(self):
        return self.title


class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    video_url = models.URLField(blank=True, null=True)
    short_description = models.CharField(max_length=255)
    content = models.TextField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', null=True, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.comment_text[:20]}"


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title
