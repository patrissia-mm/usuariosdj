from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from django.views.generic import (
    View, 
    CreateView
)

from django.views.generic.edit import (
    FormView
)

from .forms import (
    UserRegisterForm, 
    LoginForm,
    UpdatePasswordForm,
    VerificationForm
)

from .models import User

from .functions import code_generator

# class UserRegisterView(CreateView):
class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    # Direccionar a la raiz
    success_url = '/'

    #para que un FormView ejecute un proceso, en este caso un post guardado, debe tener la siguiente función
    def form_valid(self, form):
        #Generar código aleatorio
        codigo = code_generator()
        # escribir el proceso que se desee hacer, en este caso se usará el modelo User, para registrarlo con el manager create_user
        #puedo o no almacenar estos datos en una instancia (usuario), en este caso se necesita para recuperar el id al momento de validar el código de registro
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            #extra_fields:
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos'],
            genero = form.cleaned_data['genero'],
            codregistro = codigo
        )
        #enviar el email con el código aleatorio generado
        asunto = 'Confirmación de creación de Usuario'
        mensaje = 'El código generado es: ' + codigo
        remitente = 'patriciamedinameneses@gmail.com'
        #
        send_mail(asunto, mensaje, remitente, [form.cleaned_data['email'],])
        # return super(UserRegisterView, self).form_valid(form)
        # redirigir a una página para introducri el código
        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification',
                kwargs={'pk':usuario.id}
            )
        )
    
class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        user = authenticate(
            username= form.cleaned_data['username'],
            password= form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        #redirigir al usuario a otra pantalla, para hacer esto dentro de un proceso usar el HTTPREsponse redirect
        return HttpResponseRedirect(
            reverse('users_app:user-login')
        )
    
class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')
    def form_valid(self,form):
        #leer el usuario logueado
        usuario = self.request.user
        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data['password1']
        )
        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()
        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)

class CodeVerificationView(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user-login')

    #redefiniendo la función get_form_kwargs para enviar l formulario el PK que se está recibiendo en la vista
    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk'],
        })
        return kwargs

    def form_valid(self, form):
        #Sí el usuario cumple con la validación, cambiar su estado a active
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active = True
        )
        return super(CodeVerificationView, self).form_valid(form)
