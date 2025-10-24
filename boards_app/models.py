from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="boards_member_of", blank=True)
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,  # Was passiert, wenn der User gelöscht wird?
        related_name="boards_owned"  # Name für den "Rückweg"
    )

    def __str__(self):
        return self.title
    

class Ticket(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tickets")
    status = models.CharField(max_length=20)
    priority = models.CharField(max_length=20)