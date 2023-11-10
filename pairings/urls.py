from django.urls import path
from django.views.generic.base import TemplateView


from .views import pair_students

urlpatterns = [
    path('pairs/',pair_students,name='pairs'),
    path('interests',TemplateView.as_view(template_name='interest.html'),name='interests'),
]
