from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit

from .models import User


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number', 'username', 'email']
        widgets = {
            'phone_number': forms.TextInput(attrs={"placeholder": "Phone number"}),
            'username': forms.TextInput(attrs={"placeholder": "Username"}),
            'email': forms.EmailInput(attrs={"placeholder": "Email"}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
        for visible in self.visible_fields():
            visible.field.widget.attrs['aria-required'] = 'true'
            visible.field.widget.attrs['class'] = 'form-control-sm pl-3'
            
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        if (password1 == '' and password2 != '') or (password2 == '' and password1 != ''):
            raise ValidationError("Passwords do not match.")
        if password1 != '' and password2 != '':
            if self.instance.check_password(password2):
                return self.add_error('password1', 'You have inserted your current password.')
            try:
                validate_password(password2, user=self.instance)
            except ValidationError as error:
                return self.add_error('password1', error)
        return password2

    def save(self, commit=True, request=None):
        password = self.cleaned_data['password2']
        user = super().save(commit=False)
        if password != '' and request:
            user.set_password(password)
            login(request, user)
        if commit:
            user.save()
        return user
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password confirmation"}))



class UserChangeForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['avatar', 'phone_number', 'username', 'email', 'first_name', 'last_name', 'gender', 'date_of_birth', 'country', 'city', 'biography']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'max': datetime.now().date(), 'min': datetime(1920, 1, 1).date()}),
            }
        
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div('avatar', 'phone_number', 'username', 'email'),
            Div('first_name', 'last_name', 'gender', 'date_of_birth'),
            Div('country', 'city', 'biography'),
            Div('password1', 'password2'),
            Div(Submit('save', 'save', css_class="btn btn-primary btn-lg"))
        )

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "leave empty, if you don't wish to change"}), required=False)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={"placeholder": "leave empty, if you don't wish to change"}), required=False)
