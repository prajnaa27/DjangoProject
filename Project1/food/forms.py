from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'required': True}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'required': True, 'rows': 5}),
        }
