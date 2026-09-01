from django import forms

class PhoneForm(forms.Form):
    phone = forms.CharField(
        max_length = 11,
        label = 'شماره موبایل',
        widget=forms.TextInput(attrs={
            'placeholder': '09xxxxxxxxx'
        })
    )

class OtpForm(forms.Form):
    code = forms.CharField(
        max_length= 6,
        label='کد تایید',
        widget=forms.TextInput(attrs={
            'palceholder': 'کدارسال شده'
        })
    )