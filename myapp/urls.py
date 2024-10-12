from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list, name='course-list'),
    path('courses/<int:id>/', views.course_lessons, name='course-lessons'),  # Without course name, will redirect
    path('courses/<int:id>=<str:course_name>/', views.course_lessons, name='course-lessons-with-name'),  # With course name
]
