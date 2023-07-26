from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import *

class AdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
   
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user



class DoctorUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,label='Password')
   
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def __init__(self,*args, **kwargs):

        super().__init__(*args, **kwargs)
        for frm in self.fields.values():
            frm.widget.attrs['class']='form-control'
            frm.widget.attrs['placeholder']=frm.label

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'],)
        if commit:
            user.save()
        return user
    
    
class DoctorForm(forms.ModelForm):
    CHOICES = [('Male','Male'),('Female','Female'),('Other','Other')]
    gender = forms.ChoiceField(widget=forms.RadioSelect(),choices=CHOICES)
    department = forms.ModelChoiceField(queryset=Department.objects.all(),empty_label='Select Department',)
    
    class Meta:
        model = Doctor
        fields = ['dob','address','profile_pic','mobileno','gender','dob']

    def __init__(self,*args, **kwargs):
        
        super().__init__(*args, **kwargs)
        for frm in self.fields.values():
            # frm.widget.attrs['class']='form-control'
            frm.widget.attrs['placeholder']=frm.label

class PatientUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,label='Password')
   
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def __init__(self,*args, **kwargs):

        super().__init__(*args, **kwargs)
        for frm in self.fields.values():
            frm.widget.attrs['class']='form-control'
            frm.widget.attrs['placeholder']=frm.label

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'],)
        if commit:
            user.save()
        return user
    
    
class PatientForm(forms.ModelForm):
    CHOICES = [('Male','Male'),('Female','Female'),('Other','Other')]
    gender = forms.ChoiceField(widget=forms.RadioSelect(),choices=CHOICES)
    assignedDoctorId = forms.ModelChoiceField(queryset=Doctor.objects.all(),empty_label='Select Doctor')
    class Meta:
        model = Patient
        fields = ['dob','address','profile_pic','mobileno','symptoms','gender']

    def __init__(self,*args, **kwargs):
        
        super().__init__(*args, **kwargs)
        for frm in self.fields.values():
            # frm.widget.attrs['class']='form-control'
            frm.widget.attrs['placeholder']=frm.label

