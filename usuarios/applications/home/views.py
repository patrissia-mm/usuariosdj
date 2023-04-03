import datetime
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from django.views.generic import(
    TemplateView
)

#Mixin para ser reutilizado en varias vistas
class FechaMixin(object):

    def get_context_data(self, **kwargs):
        context = super(FechaMixin, self).get_context_data(**kwargs)
        context['fecha'] = datetime.datetime.now()
        return context

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home/index.html'
    #Sí el usuario no está logueado, se le redirige a la página de login
    login_url = reverse_lazy('users_app:user-login')


class TemplatePruebaMixin(FechaMixin, TemplateView):
    template_name = "home/mixin.html"
    

    
