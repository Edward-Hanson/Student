from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class StudentBackend(ModelBackend):
    def authenticate(self,request,student_id=None,password=None,**kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(student_id=student_id)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            return None