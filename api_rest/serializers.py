from rest_framework import serializers
from django.db.models import Sum
from django.contrib.auth.hashers import make_password
from .models import Usuario, Musica, Album, Faixa, MusicaDoDia, AlbumDaSemana, Review


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'user_username', 'user_email', 'user_password',
            'user_bio', 'user_avatar', 'is_admin'
        ]
        read_only_fields = ['is_admin']
        extra_kwargs = {
            'user_password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('user_password', '')
        usuario = Usuario(**validated_data)
        if password:
            usuario.user_password = make_password(password)
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop('user_password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.user_password = make_password(password)

        instance.save()
        return instance


class MusicaSerializer(serializers.ModelSerializer):
    review_count = serializers.SerializerMethodField()
    review_likes = serializers.SerializerMethodField()
    review_dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Musica
        fields = [
            'id', 'titulo', 'artista', 'album_nome', 'genero', 'duracao_ms',
            'capa_url', 'spotify_id', 'likes', 'dislikes', 'criado_em',
            'review_count', 'review_likes', 'review_dislikes'
        ]

    def get_review_count(self, obj):
        return obj.reviews_musicas.count()

    def get_review_likes(self, obj):
        return obj.reviews_musicas.aggregate(total=Sum('likes'))['total'] or 0

    def get_review_dislikes(self, obj):
        return obj.reviews_musicas.aggregate(total=Sum('dislikes'))['total'] or 0


class FaixaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faixa
        fields = ['id', 'titulo', 'duracao_ms', 'numero']


class AlbumSerializer(serializers.ModelSerializer):
    faixas = FaixaSerializer(many=True, read_only=True)
    review_count = serializers.SerializerMethodField()
    review_likes = serializers.SerializerMethodField()
    review_dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = [
            'id', 'titulo', 'artista', 'ano', 'genero', 'capa_url',
            'spotify_id', 'likes', 'dislikes', 'criado_em', 'faixas',
            'review_count', 'review_likes', 'review_dislikes'
        ]

    def get_review_count(self, obj):
        return obj.reviews_albuns.count()

    def get_review_likes(self, obj):
        return obj.reviews_albuns.aggregate(total=Sum('likes'))['total'] or 0

    def get_review_dislikes(self, obj):
        return obj.reviews_albuns.aggregate(total=Sum('dislikes'))['total'] or 0


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


class ReviewSerializer(serializers.ModelSerializer):
    usuario_username = serializers.SerializerMethodField()
    alvo_tipo = serializers.SerializerMethodField()
    alvo_titulo = serializers.SerializerMethodField()
    alvo_artista = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'usuario', 'usuario_username', 'autor_nome', 'musica', 'album',
            'texto', 'likes', 'dislikes', 'criado_em', 'alvo_tipo', 'alvo_titulo', 'alvo_artista'
        ]
        read_only_fields = ['likes', 'dislikes', 'criado_em']

    def get_usuario_username(self, obj):
        if obj.usuario:
            return obj.usuario.user_username
        return obj.autor_nome

    def get_alvo_tipo(self, obj):
        if obj.musica:
            return 'musica'
        if obj.album:
            return 'album'
        return None

    def get_alvo_titulo(self, obj):
        if obj.musica:
            return obj.musica.titulo
        if obj.album:
            return obj.album.titulo
        return None

    def get_alvo_artista(self, obj):
        if obj.musica:
            return obj.musica.artista
        if obj.album:
            return obj.album.artista
        return None

