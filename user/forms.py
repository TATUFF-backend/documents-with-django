from django import forms

from user.models import User


class LoginForm(forms.ModelForm):
    username = forms.CharField(
        label='Username', max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'form-control form-control-lg',
                'id': 'username'
            }
        )
    )
    password = forms.CharField(
        label='Password', required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control form-control-lg',
                'id': 'password1'
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username does not exist')
        user = User.objects.get(username=username)
        if not user.check_password(password):
            raise forms.ValidationError('Incorrect password')
        self.cleaned_data['user'] = self.get_user()
        return self.cleaned_data

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)
