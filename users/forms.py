from django import forms
from .models import User


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'password', 'phone', 'verified']

    widgets = {
        'password': forms.PasswordInput(),  # To display the password field as a password input
    }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)


class UserSMSVerificationForm(forms.Form):
    verification_code = forms.CharField(max_length=6, required=True, label="Verification Code")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['password', 'activated_invite_code', 'invite_code', 'verified', 'date_joined']


class UserVerificationForm(forms.Form):
    verification_code = forms.CharField(
        label='Verification Code',
        max_length=6,
        widget=forms.TextInput(attrs={'placeholder': 'Enter the verification code'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        phone = kwargs.pop('phone', None)
        super(UserVerificationForm, self).__init__(*args, **kwargs)
        if phone:
            self.fields['phone'] = forms.CharField(
                label='Phone Number',
                max_length=20,
                initial=phone,  # Initialize the field with the phone number
                widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
                required=True
            )


class EnterInviteCodeForm(forms.Form):
    invite_code = forms.CharField(max_length=6, required=False, label='Enter Invite Code')
