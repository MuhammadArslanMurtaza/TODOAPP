from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

def generateUUID():
    return str(uuid4())

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=30)
    about = models.TextField()

    def __str__(self):
        return 'username={0}'.format(self.user.username)

class Todolist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.TextField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return 'username={0}'.format(self.user.username)