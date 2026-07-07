from urllib import request

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404

from .models import Usuario
from .serializers import UsuarioSerializer

import json
# Create your views here.


# def databaseDjango():
#     data = Usuario.objects.get(pk='trambolho')          #objeto
#     data = Usuario.objects.filter(pk='trambolho')       #queryset
#     data = Usuario.objects.exclude()                    #queryset

#     data.save()
#     data.delete()

# GET ALL USERS
@api_view(['GET'])
def get_users(request):
  
    if request.method == 'GET':
        users = Usuario.objects.all()
        serializer = UsuarioSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)

#GET USER BY USERNAME
@api_view(['GET'])
def get_user_by_username(request, username):
    try:
        user = Usuario.objects.get(user_username=username)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UsuarioSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)

#GET USER BY PK
@api_view(['GET'])
def get_user_by_pk(request, pk):
    try:
        user = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UsuarioSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


def _perfil_payload(usuario):
    reviews = Review.objects.filter(usuario=usuario).select_related('musica', 'album').order_by('-criado_em')
    payload = UsuarioSerializer(usuario).data
    payload['review_count'] = reviews.count()
    payload['reviews'] = ReviewSerializer(reviews, many=True).data
    return payload


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def perfil_usuario(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(_perfil_payload(usuario), status=status.HTTP_200_OK)

    if request.method in ['PUT', 'PATCH']:
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            usuario.refresh_from_db()
            return Response(_perfil_payload(usuario), status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_400_BAD_REQUEST)


#USER MANAGER
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_manager(request, pk=None):

    #EXEMPLE URL: http://localhost:8000/api/data/

    if request.method == 'GET':
        if pk is not None:
            try:
                user = Usuario.objects.get(pk=pk)
            except Usuario.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = UsuarioSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            users = Usuario.objects.all()
            serializer = UsuarioSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

#EXEMPLE URL: http://localhost:8000/api/data/ with POST method and body:
# {
#     "user_username": "john_doe",
#     "user_email": "john@example.com"
#     "user_password": "password123"
# }

    elif request.method == 'POST':
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#EXEMPLE URL: http://localhost:8000/api/data/1/ with PUT method and body:
# {
#     "user_username": "john_doe_updated",
#     "user_email": "john.updated@example.com",
#     "user_password": "newpassword123"
# }

    elif request.method == 'PUT':
        user_id = request.data.get('id') 
        
        if not user_id:
            return Response({"error": "ID não fornecido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            updated_user = Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "ID inválido"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UsuarioSerializer(updated_user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


    elif request.method == 'DELETE':
            # Tenta pegar o ID do corpo do JSON caso o pk da URL seja None
            user_id = pk if pk else request.data.get('id')
            
            if user_id:
                try:
                    user = Usuario.objects.get(pk=user_id)
                    user.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                except (Usuario.DoesNotExist, ValueError):
                    return Response({"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)
            
            return Response({"error": "ID não fornecido"}, status=status.HTTP_400_BAD_REQUEST)
    
#login e registro de usuário podem ser feitos usando os endpoints acima, basta enviar os dados corretos no corpo da requisição.

@api_view(['POST'])
def login(request):
    email = request.data.get('user_email')
    password = request.data.get('user_password')

    try:
        user = Usuario.objects.get(user_email=email)
        if not check_password(password, user.user_password): 
            if user.user_password == password:
                user.user_password = make_password(password)
                user.save(update_fields=['user_password'])
            else:
                return Response({"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UsuarioSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Usuario.DoesNotExist:
        return Response({"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

#registro de usuário
@api_view(['POST'])
def register(request):
    serializer = UsuarioSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        if not Usuario.objects.exclude(pk=user.pk).exists():
            user.is_admin = True
        user.save()
        return Response(UsuarioSerializer(user).data, status=201)

    return Response(
        {
            "serializer_errors": serializer.errors,
            "received_data": request.data,
        },
        status=400
    )


from django.http import JsonResponse
def ping(request):
    return JsonResponse({"pong": True})


# =============================================
# SPOTIFY, MUSICAS, ALBUNS, ROTAÇÃO, BUSCA
# =============================================

from collections import defaultdict
from datetime import date, timedelta
from django.db.models import Q, F, Avg, Count
from .models import Musica, Album, Faixa, MusicaDoDia, AlbumDaSemana, Reacao
from .serializers import (
    MusicaSerializer, AlbumSerializer,
    MusicaDoDiaSerializer, AlbumDaSemanaSerializer,
)
from .models import Review
from .serializers import ReviewSerializer
from . import spotify


# --- Admin helper ---

def _is_admin(request):
    user_id = request.query_params.get('usuario_id') or request.data.get('usuario_id')
    if not user_id:
        return False
    try:
        return Usuario.objects.get(pk=user_id).is_admin
    except (Usuario.DoesNotExist, ValueError, TypeError):
        return False


# --- Spotify Search & Add ---

@api_view(['GET'])
def spotify_search(request):
    if not _is_admin(request):
        return Response({"error": "Acesso restrito a administradores"}, status=status.HTTP_403_FORBIDDEN)

    query = request.query_params.get('q', '')
    search_type = request.query_params.get('type', 'track')

    if not query:
        return Response({"error": "Parâmetro 'q' é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

    results = spotify.search_spotify(query, search_type)
    if results is None:
        return Response({"error": "Falha ao conectar com Spotify. Verifique as credenciais."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(results, status=status.HTTP_200_OK)


@api_view(['POST'])
def spotify_add_track(request):
    if not _is_admin(request):
        return Response({"error": "Acesso restrito a administradores"}, status=status.HTTP_403_FORBIDDEN)

    spotify_id = request.data.get('spotify_id')
    titulo = request.data.get('titulo', '')
    artista = request.data.get('artista', '')
    album_nome = request.data.get('album_nome', '')
    genero = request.data.get('genero', '')
    duracao_ms = request.data.get('duracao_ms', 0)
    capa_url = request.data.get('capa_url', '')

    if not spotify_id or not titulo:
        return Response({"error": "spotify_id e titulo são obrigatórios"}, status=status.HTTP_400_BAD_REQUEST)

    musica, created = Musica.objects.get_or_create(
        spotify_id=spotify_id,
        defaults={
            'titulo': titulo,
            'artista': artista,
            'album_nome': album_nome,
            'genero': genero,
            'duracao_ms': duracao_ms,
            'capa_url': capa_url,
        }
    )

    serializer = MusicaSerializer(musica)
    http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
    return Response(serializer.data, status=http_status)


@api_view(['POST'])
def spotify_add_album(request):
    if not _is_admin(request):
        return Response({"error": "Acesso restrito a administradores"}, status=status.HTTP_403_FORBIDDEN)

    spotify_id = request.data.get('spotify_id')
    titulo = request.data.get('titulo', '')
    artista = request.data.get('artista', '')
    ano = request.data.get('ano')
    genero = request.data.get('genero', '')
    capa_url = request.data.get('capa_url', '')

    if not spotify_id or not titulo:
        return Response({"error": "spotify_id e titulo são obrigatórios"}, status=status.HTTP_400_BAD_REQUEST)

    album, created = Album.objects.get_or_create(
        spotify_id=spotify_id,
        defaults={
            'titulo': titulo,
            'artista': artista,
            'ano': ano,
            'genero': genero,
            'capa_url': capa_url,
        }
    )

    if created:
        tracks_response = spotify.get_album_tracks(spotify_id)
        if tracks_response and 'items' in tracks_response:
            for i, t in enumerate(tracks_response['items']):
                Faixa.objects.create(
                    album=album,
                    titulo=t.get('name', ''),
                    duracao_ms=t.get('duration_ms', 0),
                    numero=t.get('track_number', i + 1),
                )

    serializer = AlbumSerializer(album)
    http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
    return Response(serializer.data, status=http_status)


# --- Listagem local ---

@api_view(['GET'])
def listar_musicas(request):
    musicas = Musica.objects.all().order_by('-criado_em')
    serializer = MusicaSerializer(musicas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def detalhe_musica(request, musica_id):
    musica = get_object_or_404(Musica, pk=musica_id)
    data = MusicaSerializer(musica).data

    usuario_id = request.query_params.get('usuario_id')
    if usuario_id:
        try:
            reacao = Reacao.objects.get(usuario_id=usuario_id, musica=musica)
            data['user_reaction'] = reacao.tipo
        except (Reacao.DoesNotExist, ValueError):
            data['user_reaction'] = None

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def listar_albuns(request):
    albuns = Album.objects.all().order_by('-criado_em')
    serializer = AlbumSerializer(albuns, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def detalhe_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    data = AlbumSerializer(album).data

    usuario_id = request.query_params.get('usuario_id')
    if usuario_id:
        try:
            reacao = Reacao.objects.get(usuario_id=usuario_id, album=album)
            data['user_reaction'] = reacao.tipo
        except (Reacao.DoesNotExist, ValueError):
            data['user_reaction'] = None

    return Response(data, status=status.HTTP_200_OK)


# --- Rotação automática (Lazy) ---

@api_view(['GET'])
def musica_do_dia(request):
    hoje = date.today()

    try:
        entrada = MusicaDoDia.objects.get(data=hoje)
    except MusicaDoDia.DoesNotExist:
        trinta_dias_atras = hoje - timedelta(days=30)
        ids_recentes = MusicaDoDia.objects.filter(
            data__gte=trinta_dias_atras
        ).values_list('musica_id', flat=True)

        disponiveis = Musica.objects.exclude(id__in=ids_recentes)
        if not disponiveis.exists():
            disponiveis = Musica.objects.all()

        if not disponiveis.exists():
            return Response({"error": "Nenhuma música cadastrada"}, status=status.HTTP_404_NOT_FOUND)

        musica_escolhida = disponiveis.order_by('?').first()
        entrada = MusicaDoDia.objects.create(musica=musica_escolhida, data=hoje)

    serializer = MusicaDoDiaSerializer(entrada)
    data = serializer.data

    usuario_id = request.query_params.get('usuario_id')
    if usuario_id:
        try:
            reacao = Reacao.objects.get(usuario_id=usuario_id, musica=entrada.musica)
            data['user_reaction'] = reacao.tipo
        except (Reacao.DoesNotExist, ValueError):
            data['user_reaction'] = None

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def album_da_semana(request):
    hoje = date.today()
    segunda = hoje - timedelta(days=hoje.weekday())

    try:
        entrada = AlbumDaSemana.objects.get(semana_inicio=segunda)
    except AlbumDaSemana.DoesNotExist:
        sessenta_dias_atras = hoje - timedelta(days=60)
        ids_recentes = AlbumDaSemana.objects.filter(
            semana_inicio__gte=sessenta_dias_atras
        ).values_list('album_id', flat=True)

        disponiveis = Album.objects.exclude(id__in=ids_recentes)
        if not disponiveis.exists():
            disponiveis = Album.objects.all()

        if not disponiveis.exists():
            return Response({"error": "Nenhum álbum cadastrado"}, status=status.HTTP_404_NOT_FOUND)

        album_escolhido = disponiveis.order_by('?').first()
        entrada = AlbumDaSemana.objects.create(album=album_escolhido, semana_inicio=segunda)

    serializer = AlbumDaSemanaSerializer(entrada)
    data = serializer.data

    usuario_id = request.query_params.get('usuario_id')
    if usuario_id:
        try:
            reacao = Reacao.objects.get(usuario_id=usuario_id, album=entrada.album)
            data['user_reaction'] = reacao.tipo
        except (Reacao.DoesNotExist, ValueError):
            data['user_reaction'] = None

    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def definir_album_da_semana(request):
    if not _is_admin(request):
        return Response({"error": "Acesso restrito a administradores"}, status=status.HTTP_403_FORBIDDEN)

    album_id = request.data.get('album_id')
    if not album_id:
        return Response({"error": "album_id é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

    album = get_object_or_404(Album, pk=album_id)
    hoje = date.today()
    segunda = hoje - timedelta(days=hoje.weekday())

    entrada, _ = AlbumDaSemana.objects.update_or_create(
        semana_inicio=segunda,
        defaults={'album': album}
    )

    serializer = AlbumDaSemanaSerializer(entrada)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def definir_musica_do_dia(request):
    if not _is_admin(request):
        return Response({"error": "Acesso restrito a administradores"}, status=status.HTTP_403_FORBIDDEN)

    musica_id = request.data.get('musica_id')
    if not musica_id:
        return Response({"error": "musica_id é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

    musica = get_object_or_404(Musica, pk=musica_id)
    hoje = date.today()

    entrada, _ = MusicaDoDia.objects.update_or_create(
        data=hoje,
        defaults={'musica': musica}
    )

    serializer = MusicaDoDiaSerializer(entrada)
    return Response(serializer.data, status=status.HTTP_200_OK)


# --- Histórico ---

@api_view(['GET'])
def historico_musicas(request):
    entradas = MusicaDoDia.objects.select_related('musica').order_by('-data')[:7]
    serializer = MusicaDoDiaSerializer(entradas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def historico_albuns(request):
    entradas = AlbumDaSemana.objects.select_related('album').order_by('-semana_inicio')[:4]
    serializer = AlbumDaSemanaSerializer(entradas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_reviews(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    reviews = Review.objects.filter(usuario=usuario).select_related('musica', 'album').order_by('-criado_em')
    return Response(ReviewSerializer(reviews, many=True).data, status=status.HTTP_200_OK)


# --- Busca local ---

@api_view(['GET'])
def busca(request):
    query = request.query_params.get('q', '')
    tipo = request.query_params.get('tipo', 'todos')
    genero = request.query_params.get('genero', '')
    ordenar = request.query_params.get('ordenar', 'recente')

    ordem_map = {
        'recente': '-criado_em',
        'likes': '-likes',
        'titulo': 'titulo',
    }
    ordem = ordem_map.get(ordenar, '-criado_em')

    musicas_data = []
    albuns_data = []

    if tipo in ('todos', 'musica'):
        qs = Musica.objects.all()
        if query:
            qs = qs.filter(
                Q(titulo__icontains=query) | Q(artista__icontains=query) | Q(genero__icontains=query)
            )
        if genero:
            qs = qs.filter(genero__iexact=genero)
        musicas_data = MusicaSerializer(qs.order_by(ordem), many=True).data

    if tipo in ('todos', 'album'):
        qs = Album.objects.all()
        if query:
            qs = qs.filter(
                Q(titulo__icontains=query) | Q(artista__icontains=query) | Q(genero__icontains=query)
            )
        if genero:
            qs = qs.filter(genero__iexact=genero)
        albuns_data = AlbumSerializer(qs.order_by(ordem), many=True).data

    generos_musica = list(Musica.objects.exclude(genero='').values_list('genero', flat=True).distinct())
    generos_album = list(Album.objects.exclude(genero='').values_list('genero', flat=True).distinct())
    generos = sorted(set(generos_musica + generos_album))

    return Response({
        "musicas": musicas_data,
        "albuns": albuns_data,
        "generos": generos,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def busca_spotify(request):
    query = request.query_params.get('q', '')
    search_type = request.query_params.get('type', 'track')

    if not query:
        return Response({"error": "Parâmetro 'q' é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

    results = spotify.search_spotify(query, search_type)
    if results is None:
        return Response({"error": "Falha ao conectar com Spotify"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(results, status=status.HTTP_200_OK)


@api_view(['POST'])
def garantir_musica(request):
    spotify_id = request.data.get('spotify_id')
    titulo = request.data.get('titulo', '')
    artista = request.data.get('artista', '')
    album_nome = request.data.get('album_nome', '')
    genero = request.data.get('genero', '')
    duracao_ms = request.data.get('duracao_ms', 0)
    capa_url = request.data.get('capa_url', '')

    if not spotify_id or not titulo:
        return Response({"error": "spotify_id e titulo são obrigatórios"}, status=status.HTTP_400_BAD_REQUEST)

    musica, _ = Musica.objects.get_or_create(
        spotify_id=spotify_id,
        defaults={
            'titulo': titulo, 'artista': artista, 'album_nome': album_nome,
            'genero': genero, 'duracao_ms': duracao_ms, 'capa_url': capa_url,
        }
    )
    return Response(MusicaSerializer(musica).data, status=status.HTTP_200_OK)


@api_view(['POST'])
def garantir_album(request):
    spotify_id = request.data.get('spotify_id')
    titulo = request.data.get('titulo', '')
    artista = request.data.get('artista', '')
    ano = request.data.get('ano')
    genero = request.data.get('genero', '')
    capa_url = request.data.get('capa_url', '')

    if not spotify_id or not titulo:
        return Response({"error": "spotify_id e titulo são obrigatórios"}, status=status.HTTP_400_BAD_REQUEST)

    album, created = Album.objects.get_or_create(
        spotify_id=spotify_id,
        defaults={
            'titulo': titulo, 'artista': artista, 'ano': ano,
            'genero': genero, 'capa_url': capa_url,
        }
    )

    if created:
        tracks_response = spotify.get_album_tracks(spotify_id)
        if tracks_response and 'items' in tracks_response:
            for i, t in enumerate(tracks_response['items']):
                Faixa.objects.create(
                    album=album,
                    titulo=t.get('name', ''),
                    duracao_ms=t.get('duration_ms', 0),
                    numero=t.get('track_number', i + 1),
                )

    return Response(AlbumSerializer(album).data, status=status.HTTP_200_OK)


def _toggle_reaction(usuario_id, target_field, target_obj, action):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    filter_kwargs = {'usuario': usuario, target_field: target_obj}

    try:
        reacao = Reacao.objects.get(**filter_kwargs)
        if reacao.tipo == action:
            reacao.delete()
            user_reaction = None
        else:
            reacao.tipo = action
            reacao.save()
            user_reaction = action
    except Reacao.DoesNotExist:
        Reacao.objects.create(usuario=usuario, tipo=action, **{target_field: target_obj})
        user_reaction = action

    target_obj.likes = Reacao.objects.filter(**{target_field: target_obj}, tipo='like').count()
    target_obj.dislikes = Reacao.objects.filter(**{target_field: target_obj}, tipo='dislike').count()
    target_obj.save(update_fields=['likes', 'dislikes'])

    return user_reaction


@api_view(['POST'])
def react_musica(request, musica_id):
    musica = get_object_or_404(Musica, pk=musica_id)
    action = request.data.get('action')
    usuario_id = request.data.get('usuario_id')

    if action not in ('like', 'dislike'):
        return Response({'error': 'Ação inválida'}, status=status.HTTP_400_BAD_REQUEST)
    if not usuario_id:
        return Response({'error': 'Faça login para reagir'}, status=status.HTTP_401_UNAUTHORIZED)

    user_reaction = _toggle_reaction(usuario_id, 'musica', musica, action)
    data = MusicaSerializer(musica).data
    data['user_reaction'] = user_reaction
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def react_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    action = request.data.get('action')
    usuario_id = request.data.get('usuario_id')

    if action not in ('like', 'dislike'):
        return Response({'error': 'Ação inválida'}, status=status.HTTP_400_BAD_REQUEST)
    if not usuario_id:
        return Response({'error': 'Faça login para reagir'}, status=status.HTTP_401_UNAUTHORIZED)

    user_reaction = _toggle_reaction(usuario_id, 'album', album, action)
    data = AlbumSerializer(album).data
    data['user_reaction'] = user_reaction
    return Response(data, status=status.HTTP_200_OK)


def _add_user_reactions_to_reviews(reviews_data, usuario_id):
    if not usuario_id:
        return
    review_ids = [r['id'] for r in reviews_data]
    user_reactions = dict(
        Reacao.objects.filter(
            usuario_id=usuario_id,
            review_id__in=review_ids
        ).values_list('review_id', 'tipo')
    )
    for r in reviews_data:
        r['user_reaction'] = user_reactions.get(r['id'])


@api_view(['GET', 'POST'])
def reviews_musica(request, musica_id):
    musica = get_object_or_404(Musica, pk=musica_id)

    if request.method == 'GET':
        reviews = Review.objects.filter(musica=musica)
        data = ReviewSerializer(reviews, many=True).data
        _add_user_reactions_to_reviews(data, request.query_params.get('usuario_id'))
        return Response(data, status=status.HTTP_200_OK)

    texto = request.data.get('texto', '').strip()
    autor_nome = request.data.get('autor_nome', '').strip()
    usuario_id = request.data.get('usuario_id')
    nota = request.data.get('nota')

    if not texto or not autor_nome:
        return Response({'error': 'texto e autor_nome são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)

    if nota is not None:
        try:
            nota = int(nota)
        except (TypeError, ValueError):
            return Response({'error': 'nota deve ser um número entre 1 e 5'}, status=status.HTTP_400_BAD_REQUEST)
        if nota < 1 or nota > 5:
            return Response({'error': 'nota deve estar entre 1 e 5'}, status=status.HTTP_400_BAD_REQUEST)

    if usuario_id:
        review, _ = Review.objects.update_or_create(
            musica=musica,
            usuario_id=usuario_id,
            defaults={'texto': texto, 'autor_nome': autor_nome, 'nota': nota},
        )
    else:
        review = Review.objects.create(
            musica=musica,
            texto=texto,
            autor_nome=autor_nome,
            nota=nota,
        )
    return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def reviews_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)

    if request.method == 'GET':
        reviews = Review.objects.filter(album=album)
        data = ReviewSerializer(reviews, many=True).data
        _add_user_reactions_to_reviews(data, request.query_params.get('usuario_id'))
        return Response(data, status=status.HTTP_200_OK)

    texto = request.data.get('texto', '').strip()
    autor_nome = request.data.get('autor_nome', '').strip()
    usuario_id = request.data.get('usuario_id')
    nota = request.data.get('nota')

    if not texto or not autor_nome:
        return Response({'error': 'texto e autor_nome são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)

    if nota is not None:
        try:
            nota = int(nota)
        except (TypeError, ValueError):
            return Response({'error': 'nota deve ser um número entre 1 e 5'}, status=status.HTTP_400_BAD_REQUEST)
        if nota < 1 or nota > 5:
            return Response({'error': 'nota deve estar entre 1 e 5'}, status=status.HTTP_400_BAD_REQUEST)

    if usuario_id:
        review, _ = Review.objects.update_or_create(
            album=album,
            usuario_id=usuario_id,
            defaults={'texto': texto, 'autor_nome': autor_nome, 'nota': nota},
        )
    else:
        review = Review.objects.create(
            album=album,
            texto=texto,
            autor_nome=autor_nome,
            nota=nota,
        )
    return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def review_reaction(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    action = request.data.get('action')
    usuario_id = request.data.get('usuario_id')

    if action not in ('like', 'dislike'):
        return Response({'error': 'Ação inválida'}, status=status.HTTP_400_BAD_REQUEST)
    if not usuario_id:
        return Response({'error': 'Faça login para reagir'}, status=status.HTTP_401_UNAUTHORIZED)

    user_reaction = _toggle_reaction(usuario_id, 'review', review, action)
    data = ReviewSerializer(review).data
    data['user_reaction'] = user_reaction
    return Response(data, status=status.HTTP_200_OK)


# --- Rankings ---

@api_view(['GET'])
def rankings(request):
    top_albuns = Album.objects.annotate(
        media=Avg('reviews_albuns__nota'),
        num_reviews=Count('reviews_albuns'),
    ).filter(media__isnull=False).order_by('-media', '-num_reviews')[:10]

    top_musicas = Musica.objects.annotate(
        media=Avg('reviews_musicas__nota'),
        num_reviews=Count('reviews_musicas'),
    ).filter(media__isnull=False).order_by('-media', '-num_reviews')[:10]

    artista_counts = defaultdict(int)
    for entry in (
        Review.objects.filter(musica__isnull=False)
        .values(artista=F('musica__artista'))
        .annotate(total=Count('id'))
    ):
        artista_counts[entry['artista']] += entry['total']
    for entry in (
        Review.objects.filter(album__isnull=False)
        .values(artista=F('album__artista'))
        .annotate(total=Count('id'))
    ):
        artista_counts[entry['artista']] += entry['total']

    top_artistas = sorted(artista_counts.items(), key=lambda x: -x[1])[:10]
    artistas_data = [{'artista': a, 'total_reviews': c} for a, c in top_artistas]

    return Response({
        'top_albuns': AlbumSerializer(top_albuns, many=True).data,
        'top_musicas': MusicaSerializer(top_musicas, many=True).data,
        'top_artistas': artistas_data,
    }, status=status.HTTP_200_OK)