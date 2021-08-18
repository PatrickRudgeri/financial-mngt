from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'app'
urlpatterns = [
    # path('', views.registrar, name="registrar"),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('', views.home, name='home'),

    path('despesas/', views.DespesaListView.as_view(), name='despesas'),
    path('receitas/', views.ReceitaListView.as_view(), name='receitas'),
    path('perfil/', views.PerfilDetailView.as_view(), name='perfil'),

    # Adicionar receitas e despesas
    # path('receitas/add/', views.add_receita, name='receita_add'),
    # path('despesas/add/', views.add_despesa, name='despesa_add'),

    # Editar receitas e despesas
    # path('receitas/<int:pk>/editar/', views.editar_receita, name='receita_edit'),
    # path('despesas/<int:pk>/editar/', views.editar_despesa, name='despesa_edit'),

    path('logout/', views.logout_user, name='logout'),
]
