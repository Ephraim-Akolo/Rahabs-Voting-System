from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class state(models.Model):
    name = models.CharField(max_length=10)


class LocalGorvernment(models.Model):
    state = models.ForeignKey(state, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)


class User(AbstractUser):

    vin = models.CharField(max_length=20, null=True, unique=True)
    lga = models.ForeignKey(LocalGorvernment, null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.username
    

class PoliticalParty(models.Model):
    name = models.CharField(max_length=10)
    

class Election(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    party = models.ForeignKey(PoliticalParty, on_delete=models.CASCADE)
    lga = models.ForeignKey(LocalGorvernment, on_delete=models.CASCADE)

