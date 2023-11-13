from django.urls import path
from django.views.generic.base import TemplateView


from .views import get_interest

urlpatterns = [
    path('get/interest',get_interest,name='get_interest'),
    path('interests',TemplateView.as_view(template_name='interest.html'),name='interests'),
]
