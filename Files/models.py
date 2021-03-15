from django.db import models


# Create your models here.
class File(models.Model):
    id = models.AutoField(primary_key=True) # Id of paste, auto increments
    type = models.CharField(max_length=100, default="text") # Type of paste, either file upload or text
    name = models.CharField(max_length=100) # Name of paste
    location = models.CharField(max_length=200) # Path of paste
    belongsto = models.IntegerField(default=0) # Userid of user who created the paste, 0 if un authenticated
    visibility = models.CharField(max_length=100, default="private") # Private or unlisted pastes
    description = models.CharField(max_length=200, default="N/A") # Description of file, displayed on dashboard
