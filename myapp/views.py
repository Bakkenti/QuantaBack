from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import redirect
from .models import Course, Lesson, Student
from .serializers import CourseSerializer, LessonSerializer, RegistrationSerializer, LoginSerializer, ModuleSerializer



@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        # Hash the password before storing it
        student = Student(
            username=serializer.validated_data['username'],
            password=make_password(serializer.validated_data['password']),  # Hash the password
        )

        student.save()
        return Response({"message": "Registration successful!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            # Fetch the student from the Student model
            student = Student.objects.get(username=username)

            # Check the password
            if check_password(password, student.password):  # Check against the hashed password
                # Logic for creating JWT token here

                return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        except Student.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])  # Public route
def course_list(request):
    """List all available courses."""
    courses = Course.objects.all()
    if not courses:
        return Response({'message': 'No courses available'})
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])  # Public route
def course_modules(request, id):
    """Retrieve modules and their lessons for a specific course."""
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return Response({'message': 'Course not found'}, status=404)

    modules = course.modules.all()  # Get all modules for the course
    if not modules:
        return Response({'message': 'No modules available for this course'})

    serializer = ModuleSerializer(modules, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])  # Public route
def course_lessons(request, id, title=None):
    """Retrieve lessons for a specific course."""
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return Response({'message': 'Course not found'}, status=404)

    if title is None or course.title != title:
        return redirect(f'/courses/{id}={course.title}/')

    lessons = course.lessons.all()
    if not lessons:
        return Response({'message': 'No lessons available'})

    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)
