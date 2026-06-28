from rest_framework import serializers
from .models import Usuario, Musica, Album, Faixa, MusicaDoDia, AlbumDaSemana


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'user_username', 'user_email', 'user_password']


class MusicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musica
        fields = ['id', 'titulo', 'artista', 'album_nome', 'genero', 'duracao_ms', 'capa_url', 'spotify_id', 'criado_em']


class FaixaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faixa
        fields = ['id', 'titulo', 'duracao_ms', 'numero']


class AlbumSerializer(serializers.ModelSerializer):
    faixas = FaixaSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['id', 'titulo', 'artista', 'ano', 'genero', 'capa_url', 'spotify_id', 'criado_em', 'faixas']


class MusicaDoDiaSerializer(serializers.ModelSerializer):
    musica = MusicaSerializer(read_only=True)

    class Meta:
        model = MusicaDoDia
        fields = ['id', 'musica', 'data']


class AlbumDaSemanaSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(read_only=True)

    class Meta:
        model = AlbumDaSemana
        fields = ['id', 'album', 'semana_inicio']

