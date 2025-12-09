from django.db import models

# Create your models here.

class Classe (models.Model):
    name = models.CharField(max_length=50)
    


class Student(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30) 
    age = models.IntegerField()
    email = models.EmailField()
    address = models.TextField(default="Tunis")
    classe = models.ForeignKey("Classe",on_delete=models.CASCADE, null=True)

