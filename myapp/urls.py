from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list, name='course-list'),
    path('courses/<int:id>/', views.course_lessons, name='course-lessons'),
    path('courses/<int:id>=<str:title>/', views.course_lessons, name='course-lessons'),
    path('register/', views.register, name='registration'),
    path('login/', views.login, name='login'),
]
