from django.db import models


class Sala(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    has_projector = models.BooleanField(default=True)

class Rezerwacja(models.Model):
    date = models.DateField()
    comment = models.TextField()
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)