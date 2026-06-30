from django.contrib import admin
from .models import Usuario, Musica, Album, Faixa, MusicaDoDia, AlbumDaSemana, Reacao


admin.site.register(Usuario)


class FaixaInline(admin.TabularInline):
    model = Faixa
    extra = 0


@admin.register(Musica)
class MusicaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'artista', 'album_nome', 'genero']
    search_fields = ['titulo', 'artista']


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'artista', 'ano', 'genero']
    search_fields = ['titulo', 'artista']
    inlines = [FaixaInline]


@admin.register(MusicaDoDia)
class MusicaDoDiaAdmin(admin.ModelAdmin):
    list_display = ['data', 'musica']


@admin.register(AlbumDaSemana)
class AlbumDaSemanaAdmin(admin.ModelAdmin):
    list_display = ['semana_inicio', 'album']


@admin.register(Reacao)
class ReacaoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo', 'musica', 'album', 'review']
