from django.shortcuts import render

from django.views.generic.edit import (
    FormView
)

from .forms import UserRegisterForm
from .models import User

# Create your views here.

# class UserRegisterView(CreateView):
class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    # Direccionar a la raiz
    success_url = '/'

    #para que un FormView ejecute un proceso, en este caso un post guardado, debe tener la siguiente función
    def form_valid(self, form):
        # escribir el proceso que se desee hacer, en este caso se usará el modelo User, para registrarlo con el manager create_user
        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            #extra_fields:
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos'],
            genero = form.cleaned_data['genero'], 
        )
        return super(UserRegisterView, self).form_valid(form)