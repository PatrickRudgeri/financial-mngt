from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils import timezone as tz
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Receita, Despesa, User
from .forms import PerfilForm, ReceitaForm, DespesaForm
from .utils import now

import plotly.express as px
import plotly
import pandas as pd


# Function-based views
@login_required()
def home(request):
    # if request.user.is_authenticated:
    context = {'user': request.user}

    # QuerySet API reference: https://bit.ly/3gfAPHI
    receitas_user = request.user.receita_set.all().order_by('data')
    despesas_user = request.user.despesa_set.all().order_by('data')

    # receitas e despesas do mês atual
    context['receitas_mes'] = receitas_user.filter(data__month=str(now().month))
    context['despesas_mes'] = despesas_user.filter(data__month=str(now().month))

    context['total_receitas'] = 'R$ {:.2f}'.format(sum([r.valor for r in context['receitas_mes']]))
    context['total_despesas'] = 'R$ {:.2f}'.format(sum([r.valor for r in context['despesas_mes']]))
    context['today'] = now()

    # Gerando dataframes e plotando alguns gráficos de exemplo
    df_receitas = pd.DataFrame(list(context['receitas_mes'].values()))
    df_despesas = pd.DataFrame(list(context['despesas_mes'].values()))

    fig = px.bar(df_despesas, x='data', y='valor', hover_name='nome')
    context['graph_despesas'] = plotly.offline.plot(fig, auto_open=False, output_type='div')

    fig = px.bar(df_receitas, x='data', y='valor', hover_name='nome')
    context['graph_receitas'] = plotly.offline.plot(fig, auto_open=False, output_type='div')

    return render(request, 'app/home.html', context)
    # else:
    # return HttpResponse('Usuário Não autenticado')


@login_required()
def logout_user(request):
    logout(request)
    return redirect(settings.LOGIN_URL)


# Class-based views
class DespesaListView(LoginRequiredMixin, ListView):
    model = Despesa
    template_name = 'app/despesas.html'

    def get_queryset(self):
        # obtendo apenas despesas do usuario atual e mês corrente
        qs = super().get_queryset()
        qs = qs.filter(usuario=self.request.user)
        qs = qs.filter(data__month=str(now().month)).order_by('data')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #  ** Se for necessário, adicionar outras variaveis de contexto aqui
        return context


class ReceitaListView(LoginRequiredMixin, ListView):
    model = Receita
    template_name = 'app/receitas.html'

    def get_queryset(self):
        # obtendo apenas receitas do usuario atual e mês corrente
        qs = super().get_queryset()
        qs = qs.filter(usuario=self.request.user)
        qs = qs.filter(data__month=str(now().month)).order_by('data')
        return qs


class ReceitaCreateView(LoginRequiredMixin, CreateView):
    model = Receita
    template_name = 'app/add_receita.html'
    form_class = ReceitaForm

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class DespesaCreateView(LoginRequiredMixin, CreateView):
    model = Despesa
    template_name = 'app/add_despesa.html'
    form_class = DespesaForm

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class PerfilUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'app/perfil.html'
    form_class = PerfilForm
    success_url = reverse_lazy('home', urlconf='app.urls')

    def get_object(self, queryset=None):
        # Generic DetailView without a PK or Slug: https://bit.ly/3CWvA9z
        return get_object_or_404(User, pk=self.request.user.id)


class ReceitaUpdateView(LoginRequiredMixin, UpdateView):
    # view para atualizar receita
    model = Receita
    form_class = ReceitaForm
    template_name = 'app/edit_receita.html'


class DespesaUpdateView(LoginRequiredMixin, UpdateView):
    # view para atualizar despesa
    model = Despesa
    form_class = DespesaForm
    template_name = 'app/edit_despesa.html'


class ReceitaDeleteView(LoginRequiredMixin, DeleteView):
    # view para deletar receita
    model = Receita
    success_url = reverse_lazy('app:receitas')


class DespesaDeleteView(LoginRequiredMixin, DeleteView):
    # view para deletar despesa
    model = Despesa
    success_url = reverse_lazy('app:despesas')

# -------------------------------------


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
