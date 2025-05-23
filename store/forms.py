from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Formulaire d'inscription personnalisé
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['username'].widget.attrs.update({'placeholder': 'Nom d\'utilisateur'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Adresse email'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Prénom'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Nom'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Mot de passe'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirmation du mot de passe'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

# Formulaire de connexion personnalisé
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['username'].widget.attrs.update({'placeholder': 'Nom d\'utilisateur'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Mot de passe'})
