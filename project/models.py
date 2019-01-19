from django.db import models

# Create your models here.

class Test(models.Model):
	count = models.IntegerField(default=0)