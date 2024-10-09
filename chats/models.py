from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class Mychats(models.Model):
    me = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='it_me')
    frnd = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='my_frnd')
    chats = models.JSONField(default=dict)

    def __str__(self) -> str:
        return f'{self.me} chat to {self.frnd}'