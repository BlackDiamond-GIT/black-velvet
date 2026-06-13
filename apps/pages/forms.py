from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': _('Vaše jméno'),
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': _('Email'),
                'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': _('Telefon'),
                'autocomplete': 'tel',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': _('Vaše zpráva'),
                'rows': 5,
            }),
        }
