from django import forms
from .models import person,location,User_Profile

class personform(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=location.objects.all())
    class Meta:
        model = person
        fields = '__all__'
        

class locationform(forms.ModelForm):
    class Meta:
        model = location
        fields = '__all__'        

class Profile_Form(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = [
        'fname',
        'lname',
        'technologies',
        'email',
        'display_picture'
        ]