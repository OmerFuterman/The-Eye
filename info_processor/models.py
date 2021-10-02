from django.db import models

class event(models.Model):
    session_id = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    meta_data = models.JSONField()
    timestamp = models.DateField()
