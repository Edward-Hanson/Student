from django.urls import path



from .views import student_login

urlpatterns= [
    path('',student_login,name='student_login'),
]