from django.db import models
import uuid

class TimeStampModel(models.Model):
    
    id =  models.UUIDField(unique=True,default=uuid.uuid4, primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
        ordering = ['created_on']
        