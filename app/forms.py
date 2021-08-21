from django import forms
from .models import User, Receita, Despesa, CategoriaDespesa, CategoriaReceita
from .utils import now


# Forms no django: https://bit.ly/37XeZEk

class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    username = forms.CharField(label='Nome de usuário')
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput())
    first_name = forms.CharField(label='Nome')
    last_name = forms.CharField(label='Sobrenome')

    password = forms.CharField(widget=forms.PasswordInput())


class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['nome', 'valor',
                  'categoria',
                  'data']

    nome = forms.CharField(widget=forms.widgets.TextInput(attrs=dict(placeholder='Salário')))
    valor = forms.FloatField(widget=forms.widgets.TextInput(attrs=dict(placeholder='1024.00')))
    categoria = forms.CharField(required=False, empty_value=None)
    data_params = {'label': 'Data',
                   'initial': now(),
                   'widget': forms.widgets.DateTimeInput(attrs={'placeholder': 'dd/mm/yyyy hh:mm:ss'})}
    data = forms.DateTimeField(**data_params)

    def clean_categoria(self):
        cat_nome = self.cleaned_data['categoria']
        if cat_nome is None:
            cat_nome = 'Sem categoria'
        cat_nome = str(cat_nome).strip().capitalize()
        cat = CategoriaReceita.objects.get_or_create(nome=cat_nome, usuario=User.objects.all()[0])[0]
        self.cleaned_data['categoria'] = cat
        return self.cleaned_data['categoria']


class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['nome', 'valor',
                  'categoria',
                  'data']

    nome = forms.CharField(widget=forms.widgets.TextInput(attrs=dict(placeholder='Mercado')))
    valor = forms.FloatField(widget=forms.widgets.TextInput(attrs=dict(placeholder='253.90')))
    categoria = forms.CharField(required=False, empty_value=None)
    data_params = {'label': 'Data',
                   'initial': now(),
                   'widget': forms.widgets.DateTimeInput(attrs={'placeholder': 'dd/mm/yyyy hh:mm:ss'})}
    data = forms.DateTimeField(**data_params)

    def clean_categoria(self):
        print(self.fields)
        cat_nome = self.cleaned_data['categoria']
        if cat_nome is None:
            cat_nome = 'Sem categoria'
        cat_nome = str(cat_nome).strip().capitalize()
        cat = CategoriaDespesa.objects.get_or_create(nome=cat_nome, usuario=User.objects.all()[0])[0]
        self.cleaned_data['categoria'] = cat
        return self.cleaned_data['categoria']
