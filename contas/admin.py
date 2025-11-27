from django.contrib import admin
from .models import Tag, Conta


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'descricao')
    search_fields = ('nome',)


@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'valor_total', 'user')
    list_filter = ('user', 'tags')
    search_fields = ('nome', 'descricao')
