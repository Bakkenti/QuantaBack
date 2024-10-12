from django.contrib import admin
from .models import Author, Student, Course, Lesson, Post
from .forms import LessonForm

class LessonInline(admin.StackedInline):
    model = Lesson
    form = LessonForm
    extra = 1
    fields = ('name', 'content', 'short_description', 'video_url',)  # Explicitly declare the fields
    classes = ('collapse',)  # Optional: Collapse the entire inline by default

    class Media:
        # Include the custom JavaScript
        js = ('myapp/js/admin_lesson_toggle.js',)

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('course_name', 'formatted_rating', 'author')  # Customize the display of the fields

    def formatted_rating(self, obj):
        # Display rating with only one decimal place, as 1.3, 2.7, etc.
        return f'{obj.rating:.1f}'

    formatted_rating.short_description = 'Rating'

class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_name')

    def course_name(self, obj):
        return obj.course.course_name
    course_name.short_description = 'Course Name'

admin.site.register(Author)
admin.site.register(Student)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
admin.site.register(Post)
