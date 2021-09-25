from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}
    ))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}
    ))
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'password', 'confirm_password')

    def add_field_attributes(self, field_name: str, attributes: dict):
        field_attrs = {
            **attributes,
            'class': 'form-control'
        }
        self.fields[field_name].widget.attrs.update(field_attrs)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.add_field_attributes('first_name', {'placeholder': 'First Name'})
        self.add_field_attributes('last_name', {'placeholder': 'Last Name'})
        self.add_field_attributes('phone_number', {'placeholder': 'Phone Number'})
        self.add_field_attributes('email', {'placeholder': 'Email'})

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password does not match')