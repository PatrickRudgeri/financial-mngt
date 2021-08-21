from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.urls import reverse, reverse_lazy
from django.utils import timezone as tz
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django import forms
from .models import Receita, Despesa, User, CategoriaReceita, CategoriaDespesa
from .forms import PerfilForm, ReceitaForm, DespesaForm
from .utils import now

import plotly.express as px
import plotly
import pandas as pd


# Function-based views
@login_required()
def home(request):
    context = {'user': request.user}

    # QuerySet API reference: https://bit.ly/3gfAPHI
    receitas_user = request.user.receita_set.all().order_by('data')
    despesas_user = request.user.despesa_set.all().order_by('data')

    cat_receitas_user = request.user.categoriareceita_set.all()
    cat_despesas_user = request.user.categoriadespesa_set.all()
    #
    map_rec = {cat['id']: cat['nome'] for cat in cat_receitas_user.values('id', 'nome')}
    map_des = {cat['id']: cat['nome'] for cat in cat_despesas_user.values('id', 'nome')}

    # receitas e despesas do mês atual
    context['receitas_mes'] = receitas_user.filter(data__month=str(now().month))
    context['despesas_mes'] = despesas_user.filter(data__month=str(now().month))

    context['total_receitas'] = 'R$ {:.2f}'.format(sum([r.valor for r in context['receitas_mes']]))
    context['total_despesas'] = 'R$ {:.2f}'.format(sum([r.valor for r in context['despesas_mes']]))
    context['now'] = now()
    # Gerando dataframes e plotando alguns gráficos de exemplo
    df_receitas = pd.DataFrame(context['receitas_mes'].values('nome', 'valor', 'data', 'categoria'))
    df_despesas = pd.DataFrame(context['despesas_mes'].values('nome', 'valor', 'data', 'categoria'))
    df_receitas.replace({'categoria': map_rec}, inplace=True)
    df_despesas.replace({'categoria': map_des}, inplace=True)
    fig = px.pie(df_despesas, names='categoria', values='valor')
    context['graph_despesas'] = plotly.offline.plot(fig, auto_open=False, output_type='div')

    fig = px.pie(df_receitas, names='categoria', values='valor')
    context['graph_receitas'] = plotly.offline.plot(fig, auto_open=False, output_type='div')

    return render(request, 'app/home.html', context)


@login_required()
def logout_user(request):
    logout(request)
    return redirect(settings.LOGIN_URL)


# -----------------------------------------------------

# Class-based views

class DespesaListView(LoginRequiredMixin, ListView, FormView):
    model = Despesa
    template_name = 'app/despesas.html'
    context_object_name = 'despesa_list'
    form_class = DespesaForm

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

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


class ReceitaListView(LoginRequiredMixin, ListView, FormView):
    model = Receita
    template_name = 'app/receitas.html'
    context_object_name = 'receita_list'
    form_class = ReceitaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # form_fields = context['form'].fields
        # form_fields['categoria'] = forms.ModelChoiceField(queryset=self.request.user.categoriareceita_set.all(),
        #                                                   empty_label='Sem categoria', required=False)
        return context

    def get_queryset(self):
        # obtendo apenas receitas do usuario atual e mês corrente
        qs = super().get_queryset()
        qs = qs.filter(usuario=self.request.user)
        qs = qs.filter(data__month=str(now().month)).order_by('data')
        return qs


class ReceitaCreateView(LoginRequiredMixin, CreateView):
    model = Receita
    template_name = 'app/add_receita.html'  # Não é necessário
    form_class = ReceitaForm

    def form_valid(self, form):
        # Adicionando o usuário atual na receita e na categoria
        form.instance.usuario = self.request.user
        form.cleaned_data['categoria'].usuario = self.request.user
        form.cleaned_data['categoria'].save()
        return super().form_valid(form)


class DespesaCreateView(LoginRequiredMixin, CreateView):
    model = Despesa
    template_name = 'app/add_despesa.html'  # Não é necessário
    form_class = DespesaForm

    def form_valid(self, form):
        # Adicionando o usuário atual na despesa e na categoria
        form.instance.usuario = self.request.user
        form.cleaned_data['categoria'].usuario = self.request.user
        form.cleaned_data['categoria'].save()
        return super().form_valid(form)


class PerfilUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'app/perfil.html'
    form_class = PerfilForm
    success_url = reverse_lazy('home', urlconf='app.urls')

    def get_object(self, queryset=None):
        # Generic DetailView without a PK or Slug: https://bit.ly/3CWvA9z
        return get_object_or_404(User, pk=self.request.user.id)


class ReceitaUpdateView(LoginRequiredMixin, UpdateView, FormView):
    # view para atualizar receita
    model = Receita
    form_class = ReceitaForm
    template_name = 'app/edit_receita.html'
    pk_url_kwarg = 'id'  # padrão é pk

    def form_valid(self, form):
        # Adicionando o usuário atual na receita e na categoria
        form.instance.usuario = self.request.user
        form.cleaned_data['categoria'].usuario = self.request.user
        form.cleaned_data['categoria'].save()
        return super().form_valid(form)


class DespesaUpdateView(LoginRequiredMixin, UpdateView, FormView):
    # view para atualizar despesa
    model = Despesa
    form_class = DespesaForm
    template_name = 'app/edit_despesa.html'
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        # Adicionando o usuário atual na despesa e na categoria
        form.instance.usuario = self.request.user
        form.cleaned_data['categoria'].usuario = self.request.user
        form.cleaned_data['categoria'].save()
        return super().form_valid(form)


class ReceitaDeleteView(LoginRequiredMixin, DeleteView):
    # view para deletar receita
    model = Receita
    success_url = reverse_lazy('app:receitas')
    pk_url_kwarg = 'id'


class DespesaDeleteView(LoginRequiredMixin, DeleteView):
    # view para deletar despesa
    model = Despesa
    success_url = reverse_lazy('app:despesas')
    pk_url_kwarg = 'id'

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
