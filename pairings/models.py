from django.db import models
from django.conf import settings


# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=10)
    room_interest= models.TextField(default=None,blank=True,null=True)

    def __str__(self):
        return self.room_name
    