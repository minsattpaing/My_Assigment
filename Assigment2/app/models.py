from django.db import models


class Entry(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    degree = models.CharField(max_length=100)  # Add 'degree' field
    email = models.EmailField()  # Add 'email' field
    contact = models.CharField(max_length=20)  # Add 'contact' field

    def __str__(self):
        return self.name
