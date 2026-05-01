from django.db import models

# Create your models here.

class Usuario(models.Model):
    user_username = models.CharField(max_length=100, unique=True, default="")
    user_email = models.EmailField(unique=True, default="", max_length=254)
    user_password = models.CharField(max_length=100, default="")

    def __str__(self):
        return f'Usuario: {self.user_username}, Email: {self.user_email}'
