from django.contrib import admin

# Register your models here.
from .models import Receita, Despesa, CategoriaReceita, CategoriaDespesa

admin.site.register(Despesa)
admin.site.register(Receita)
admin.site.register(CategoriaReceita)
admin.site.register(CategoriaDespesa)
