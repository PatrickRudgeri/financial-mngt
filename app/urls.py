from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

# Sobre URLs no Django: https://docs.djangoproject.com/pt-br/3.2/topics/http/urls/#url-dispatcher

app_name = 'app'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('registrar/', views.registrar, name="registrar"),

    path('despesas/', views.DespesaListView.as_view(), name='despesas'),
    path('receitas/', views.ReceitaListView.as_view(), name='receitas'),

    # Adicionar receitas e despesas
    path('receitas/add/', views.ReceitaCreateView.as_view(), name='receita_add'),
    path('despesas/add/', views.DespesaCreateView.as_view(), name='despesa_add'),

    # Editar receitas e despesas
    path('receitas/<int:id>/editar/', views.ReceitaUpdateView.as_view(), name='receita_edit'),
    path('despesas/<int:id>/editar/', views.DespesaUpdateView.as_view(), name='despesa_edit'),

    # # Deletar receitas e despesas  (pois estamos deletando in-page diretamente por POST)
    path('receitas/<int:id>/deletar/', views.ReceitaDeleteView.as_view(), name='receita_del'),
    path('despesas/<int:id>/deletar/', views.DespesaDeleteView.as_view(), name='despesa_del'),

    path('logout/', views.logout_user, name='logout'),
    path('perfil/', views.PerfilUpdateView.as_view(), name='perfil'),

    # se for necessário utilizar regular expressions nas URLs
    # re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive, {'foo': 'bar'}), # year_arquive recebe foo=bar
]
