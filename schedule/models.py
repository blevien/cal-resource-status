from django.db import models

# Create your models here.

class Location(models.Model):
    """Model to represent a location"""
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    
class Calendar(models.Model):
    """Model to represent a calendar"""
    summary = models.CharField(max_length=500)
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.summary

class Event(models.Model):
    custom_id = models.CharField(primary_key=True, max_length=50, unique=True)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    summary = models.CharField(max_length=500)
    locations = models.ManyToManyField(Location, blank=True, related_name='locations')

    def __str__(self):
        return self.summary
    

class Display(models.Model):
    """Model to represent a display, and which calendars it has access to"""
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name