from django.db import models
from datetime import date


class Sala(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    has_projector = models.BooleanField(default=True)

    def is_reserved_today(self):
        date_today = date.today()
        if self.rezerwacja_set.filter(date=date_today).count() > 0:
            return True
        return False


class Rezerwacja(models.Model):
    date = models.DateField()
    comment = models.TextField()
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)