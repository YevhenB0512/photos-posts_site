from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import User
from django import forms


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, label='Логин')

    class Meta:
        model = User


class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].help_text = ''
        self.fields['password2'].label = 'Повтор пароля'

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )
        labels = {
            'username': 'Логин',
            'email': 'email',
        }


class ProfileEditForm(UserChangeForm):
    # image = forms.ImageField(required=False)
    # first_name = forms.CharField()
    # last_name = forms.CharField()
    # username = forms.CharField()
    # email = forms.CharField()

    class Meta:
        model = User
        fields = ('image',
                  'first_name',
                  'last_name',
                  'location',
                  'bio',)
