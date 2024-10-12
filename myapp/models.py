from django.db import models


class Author(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit id for Author
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    course_list = models.ManyToManyField('Course', blank=True, related_name='authored_courses')  # Author's course list, empty by default

    def __str__(self):
        return self.login


class Student(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit id for Student
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    subscribed_courses = models.ManyToManyField('Course', blank=True)  # Student's subscribed courses

    def __str__(self):
        return self.login


class Course(models.Model):
    course_name = models.CharField(max_length=200)
    description = models.TextField()
    course_count = models.IntegerField()
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='courses')
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Remove quotes from description
        if self.description:
            self.description = self.description.replace('"', '')
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.course_name



class Lesson(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit id for Lesson
    name = models.CharField(max_length=200)  # Lesson name
    video_url = models.URLField(blank=True, null=True)  # Optional video URL
    short_description = models.CharField(max_length=255)  # Short description of the lesson
    content = models.TextField()  # Lesson content
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')  # Each lesson belongs to a course

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit id for Post
    title = models.CharField(max_length=200)  # Blog post title
    content = models.TextField()  # Blog post content
    date_posted = models.DateTimeField(auto_now_add=True)  # Date when the post was created
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')  # Each post is associated with an author

    def __str__(self):
        return self.title
