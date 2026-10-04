from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import AdoptionRequest, Pet


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Enter password'}),
        min_length=6
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Confirm password'}),
        label="Confirm Password",
        min_length=6
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control bg-light', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Enter email address'}),
            'username': forms.TextInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Choose username'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Passwords do not match.')
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control bg-light',
            'placeholder': 'Enter your current password',
            'autocomplete': 'current-password'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control bg-light',
            'placeholder': 'Enter your new password',
            'autocomplete': 'new-password'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control bg-light',
            'placeholder': 'Confirm your new password',
            'autocomplete': 'new-password'
        })


class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['phone', 'address', 'reason', 'previous_pet_experience', 'message']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. +8801712345678'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Your complete home address'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Why do you want to adopt this pet? Share your home environment and lifestyle.'
            }),
            'previous_pet_experience': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Any additional questions or notes for the shelter staff (optional)'
            }),
        }
        labels = {
            'previous_pet_experience': 'I have owned or cared for a pet before',
            'reason': 'Why do you want this pet?',
            'message': 'Additional Message (Optional)',
        }
