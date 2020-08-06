from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm

from .models import User, Profile, Photographer, Country

class GuestForm(forms.Form):
    email    = forms.EmailField()


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['current_credit_name'].queryset = Photographer.objects.all().order_by('displayname')
        self.fields['country'].queryset = Country.objects.all().order_by('country')

    class Meta:
        model = Profile
        exclude = ('user',)
        fields = ('confirm_email', 'photo_credit_name', 'specialty','country','current_credit_name',)
        labels = {
            'photo_credit_name': 'The name you prefer to use for credit attribution',
            'current_credit_name': 'The name currently used for credit attribution in OrchidRoots. Leave blank if you do not see your name iin the list.<br>WARNING: your account will be removed if you selected name that is not yours.',
            'specialty':'Orchid related Interest. List genera or alliances of your interest',
            'confirm_email':'Confirm email',
            'country':'Country',
        }
        help_texts = {
            # 'specialty': 'List genera or alliances of orchids of your interest',
            # 'photo_credit_name': 'This is the name you prefer to use for credit attribution',
            # 'current_credit_name': 'This is the name used for credit attribution in OrchidRoots',
        }
    def clean_current_credit_name(self):
        current_credit_name = self.cleaned_data.get('current_credit_name')

        if current_credit_name and Profile.objects.filter(current_credit_name=current_credit_name).count():
            raise forms.ValidationError('This credit name has already been taken!')
        return current_credit_name


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','email','fullname',)
        labels = {
            'username':'User name',
            'email':'Email address',
            'fullname':'Full name',
        }
        help_texts = {
            'specialty': 'Orchid genera or alliances that you are interested in',
        }

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if username and User.objects.filter(username__iexact=username).count():
            raise forms.ValidationError('This username has already been taken!')
        return username


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        # user.active = False     #email confirmation before activate
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','email')
        # fields = ('username','email','fullname','specialty')

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        # fields = ('username','email', 'password', 'active', 'admin')
        fields = ('username','email', 'password')

    def clean_password(self):
        return self.initial["password"]


# TODO: Couldn't get this to work
# class SetPasswordForm(forms.Form):
#     """
#     A form that lets a user change set their password without entering the old
#     password
#     """
#     error_messages = {
#         'password_mismatch': _("The two password fields didn't match."),
#     }
#     new_password1 = forms.CharField(label=_("New password"),
#                                     widget=forms.PasswordInput)
#     new_password2 = forms.CharField(label=_("New password confirmation"),
#                                     widget=forms.PasswordInput)
#
#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super(SetPasswordForm, self).__init__(*args, **kwargs)
#
#     def clean_new_password2(self):
#         password1 = self.cleaned_data.get('new_password1')
#         password2 = self.cleaned_data.get('new_password2')
#         if password1 and password2:
#             if password1 != password2:
#                 raise forms.ValidationError(
#                     self.error_messages['password_mismatch'],
#                     code='password_mismatch',
#                 )
#         return password2
#
#     def save(self, commit=True):
#         self.user.set_password(self.cleaned_data['new_password1'])
#         if commit:
#             self.user.save()
#         return self.user