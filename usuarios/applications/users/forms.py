from django import forms
from django.contrib.auth import authenticate

from .models import User

class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label = 'Contraseña',
        required = True,
        widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )    
    )

    password2 = forms.CharField(
        label = 'Contraseña',
        required = True,
        widget = forms.PasswordInput(
            attrs={
                'placeholder' : 'Repetir contraseña'
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero',
        )

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')
        # if len(self.cleaned_data['password1']) < 5:
        #     self.add_error('password1', "La contraseña no puede ser menor a 5 caracteres")

            

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username'
            }
        )
    )

    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )

    #Función por defecto para validar varios campos de formulario
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Los datos de login no son correctos')
        return self.cleaned_data
    
class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(
        label ='Contraseña actual',
        required = True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña actual' 
            }
        )
    )

    password2 = forms.CharField(
        label='Contraseña Nueva',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder' : 'Nueva contraseña'
            }
        )
    )

class VerificationForm(forms.Form):
    codregistro = forms.CharField(required=True)

    #para recibir el pk en el formulario
    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)

    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']
        if len(codigo)==6:
            activo = User.objects.cod_validation(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError('EL código es incorrecto')
        else:
            raise forms.ValidationError('EL código es incorrecto')
