from django.db import models

# Create your models here.
class location(models.Model):
    area = models.CharField(max_length=50)
    street = models.CharField(max_length=50)

    def __str__(self):
        return "{0}_{1}".format(self.area,self.street)

class person(models.Model):
    name = models.CharField(max_length=50)
    job = models.CharField(max_length=50)
    location = models.ForeignKey(location,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class User_Profile(models.Model):
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length = 200)
    technologies = models.CharField(max_length=500)
    email = models.EmailField(default = None)
    display_picture = models.FileField()
    def __str__(self):
        return self.fname
