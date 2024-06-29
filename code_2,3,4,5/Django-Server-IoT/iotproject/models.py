from django.db import models

class values(models.Model):
    timeOn = models.IntegerField()
    timeOff = models.IntegerField()
