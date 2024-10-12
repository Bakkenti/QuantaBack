from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


@api_view(['GET'])
def course_list(request):
    courses = Course.objects.all()
    if not courses:
        return Response({'message': 'No courses available'})
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def course_lessons(request, id, course_name=None):
    try:
        # Retrieve the course by ID
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return Response({'message': 'Course not found'}, status=404)

    # If the current path does not match the expected id=course_name format, redirect
    if course_name is None or course.course_name != course_name:
        return redirect(f'/courses/{id}={course.course_name}/')

    # Retrieve related lessons
    lessons = course.lessons.all()
    if not lessons:
        return Response({'message': 'No lessons available'})

    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)