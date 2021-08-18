from django.contrib import admin

# Register your models here.
from .models import Receita, Despesa

admin.site.register(Despesa)
admin.site.register(Receita)
