from django.urls import path



from .views import student_login

urlpatterns= [
    path('login/',student_login,name='student_login'),
]