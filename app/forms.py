from django import forms
from .models import User, Receita, Despesa
from .utils import now


class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    username = forms.CharField(label='Nome de usuário')
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput())
    first_name = forms.CharField(label='Nome')
    last_name = forms.CharField(label='Sobrenome')

    # password = forms.CharField(widget=forms.PasswordInput)  # TODO: atualizar senha


class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['nome', 'valor', 'data']

    nome = forms.CharField()
    valor = forms.FloatField()
    data = forms.DateTimeField(label='Data', initial=now(),
                               widget=forms.widgets.DateTimeInput())


class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['nome', 'valor', 'data']

    nome = forms.CharField()
    valor = forms.FloatField()
    data = forms.DateTimeField(label='Data', initial=now(), widget=forms.widgets.DateTimeInput())
