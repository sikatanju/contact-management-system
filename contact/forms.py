from django import forms

from .models import Contact

class AddContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Name',
                'style': 'width: 400px'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Name',
                'style': 'width: 400px'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Name',
                'style': 'width: 400px'
            }),
            'address': forms.TextInput(attrs={
                'placeholder': 'Address',
                'style': 'width: 400px'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': "Start with '0', then add remaining 10 digits",
                'style': 'width: 400px'
            })
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone.startswith('0'):
            raise forms.ValidationError("Phone number must start with '0'.")
    
        phone_num = phone[1:]

        if not phone_num.isdigit():
            raise forms.ValidationError("Phone number must contain only digits after '0'.")
        
        if len(phone_num) != 10:
            raise forms.ValidationError("Phone number must have exactly 10 digits after '0'.")

        return phone
    
class UpdateContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone.startswith('0'):
            raise forms.ValidationError("Phone number must start with '0'.")
    
        phone_num = phone[1:]

        if not phone_num.isdigit():
            raise forms.ValidationError("Phone number must contain only digits after '0'.")
        
        if len(phone_num) != 10:
            raise forms.ValidationError("Phone number must have exactly 10 digits after '0'.")

        return phone
    
