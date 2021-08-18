from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Receita, Despesa, User


# @login_required()
def home(request):
    # if request.user.is_authenticated:
    context = {'user': request.user}
    return render(request, 'app/home.html', context)
    # else:
    # return HttpResponse("Usuário Não autenticado")


@login_required()
def logout_user(request):
    logout(request)
    return redirect(settings.LOGIN_URL)


class DespesaListView(ListView):
    model = Despesa
    template_name = "app/despesas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #  ** Se for necessário, adicionar outras variaveis de contexto aqui
        # context['NEW'] = "NEW_SOMETHING"
        return context


class ReceitaListView(ListView):
    model = Receita
    template_name = "app/receitas.html"


class PerfilDetailView(DetailView):
    model = User
    template_name = "app/perfil.html"

    # context_object_name = "username"

    def get_object(self, queryset=None):
        # https://chriskief.com/2012/12/29/django-generic-detailview-without-a-pk-or-slug/
        return get_object_or_404(User, pk=self.request.user.id)

# # TODO: alterar para LoginView
# def registrar(request):
#     return render(request, 'app/login.html')


# def autenticar(request):
#     print(request.POST)
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         # Redirect to a success page.
#         return request
#     else:
#         # Return an 'invalid login' error message.
#         return request
