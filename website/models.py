from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
import pytz, random

# Create your models here.


class State(models.Model):
    name = models.CharField(max_length=15, unique=True)

    def __str__(self) -> str:
        return f'{self.name}'


class LocalGorvernment(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return f'{self.name}'


class User(AbstractUser):

    vin = models.CharField(max_length=20, null=True, unique=True)
    lga = models.ForeignKey(LocalGorvernment, null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.username
    

class PoliticalParty(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f'{self.name}'


class Candidate(models.Model):
    name = models.CharField(max_length=30)
    party = models.OneToOneField(PoliticalParty, unique=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.party.name}'
    

class Election(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    # lga = models.ForeignKey(LocalGorvernment, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username}'


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=5, null=True)
    expiry = models.IntegerField(default=10)
    created = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        if datetime.now(tz=pytz.UTC) > (self.created + timedelta(minutes=self.expiry)): 
            return False
        return True
    
    def __str__(self) -> str:
        return f"{self.otp} : {self.user.username}"
    
    @classmethod
    def generate_otp(cls, instance):
        otp = ''.join(random.sample('012345689', 5))
        if isinstance(instance, User):
            otp_obj = cls.objects.create(user=instance,otp=otp)
        else:
            otp_obj = cls.objects.create(user=instance.user,otp=otp)
            instance.otp = otp_obj
            instance.save()
        return otp, otp_obj
    

class Accreditation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    image = models.ImageField(null=True)
    otp = models.ForeignKey(OTP, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f'{self.user.username}:{self.candidate.name}'
