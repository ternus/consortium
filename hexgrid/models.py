from django.db import models

# Create your models here.

class Dir:
    north, northeast,southeast,south,southwest,northwest = range(6)
    dirs = ("north", "northeast", "southeast", "south", "southwest","northwest")
    dirCaps = ("North", "Northeast", "Southeast", "South", "Southwest","Northwest")
    dabbrs = ("N", "NE", "SE", "S", "SW", "NW")

class Node(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=10)
    hex = models.IntegerField(unique=True, primary_key=True)
    quick_desc = models.CharField(max_length=200)
    dead_until_day = models.IntegerField(default=0)
    rumors_at_once = models.IntegerField(default=2)
    rumors_per_day = models.IntegerField(default=2)
    special = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
