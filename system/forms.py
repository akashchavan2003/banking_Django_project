from django import forms
from django.contrib.auth.models import User

class RegularUserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {'password': forms.PasswordInput}

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists. Please choose a different one.")
        return username

class SuperuserLoginForm(forms.Form):
    superuser_username = forms.CharField(max_length=150)
    superuser_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        superuser_username = cleaned_data.get('superuser_username')
        superuser_password = cleaned_data.get('superuser_password')
        if superuser_username and not User.objects.filter(username=superuser_username, is_superuser=True).exists():
            raise forms.ValidationError("Invalid superuser credentials. Please try again.")
        return cleaned_data
