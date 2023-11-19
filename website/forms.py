from typing import Any
from django import forms
from .models import Accreditation, User

class VotePostForm(forms.Form):
    partyName = forms.CharField()
    candidateName = forms.CharField()
    voterID = forms.CharField()
    password = forms.CharField()


class OTPForm(forms.Form):
    first = forms.IntegerField()
    second = forms.IntegerField()
    third = forms.IntegerField()
    fourth = forms.IntegerField()
    fifth = forms.IntegerField()


class EmailForm(forms.Form):
    email = forms.EmailField()

class RecoverPasswordForm(forms.Form):
    otp = forms.CharField(max_length=5, min_length=5)
    password = forms.CharField()
    verifyPassword = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('verifyPassword')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class UpdateImageForm(forms.ModelForm):
    class Meta:
        model = Accreditation
        fields = ['image']

    def __init__(self,*args, **kwargs):
        instance_id = args[0].get('instance_id')
        super(UpdateImageForm, self).__init__(*args, **kwargs)
        instance = Accreditation.objects.get(id=int(instance_id))
        self.instance = instance