from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError


# Create your models here.

from pairings.models import Room

class CustomUserManager(BaseUserManager):
    
    def create_user(self, student_id, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not student_id:
            raise ValueError("The given student identification must be set")
        user = self.model(student_id=student_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, student_id=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(student_id, password, **extra_fields)



class CustomUser(AbstractUser):
    username = None
    last_name = None
    email = None

    student_name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=10, unique=True)
    student_programme = models.CharField(max_length=50, blank=True, null=True)
    student_level = models.PositiveIntegerField(blank=True, null=True)
    student_mail = models.EmailField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE,related_name="students",null=True)
    objects = CustomUserManager()
       
    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = ['student_name']

    def __str__(self):
        return self.student_id


class Student_Interest(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='interests', blank=True, null=True)
    interest = models.CharField(max_length=25)

    def save(self, *args, **kwargs):
        if self.student.interests.count() > 4:
            raise ValidationError("A student can have up to 4 interests.")
        if self.student.interests.filter(interest=self.interest).exists():
            raise ValidationError("This interest is already added for the student.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.interest