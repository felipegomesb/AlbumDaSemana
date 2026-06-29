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
        user.user_password = make_password(user.user_password)
        user.save()
        return Response(serializer.data, status=201)

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

from datetime import date, timedelta
from django.db.models import Q
from .models import Musica, Album, Faixa, MusicaDoDia, AlbumDaSemana
from .serializers import (
    MusicaSerializer, AlbumSerializer,
    MusicaDoDiaSerializer, AlbumDaSemanaSerializer,
)
from .models import Review
from .serializers import ReviewSerializer
from . import spotify


# --- Spotify Search & Add ---

@api_view(['GET'])
def spotify_search(request):
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
    spotify_id = request.data.get('spotify_id')
    titulo = request.data.get('titulo', '')
    artista = request.data.get('artista', '')
    ano = request.data.get('ano')
    genero = request.data.get('genero', '')
    capa_url = request.data.get('capa_url', '')
    faixas_data = request.data.get('faixas', [])
    
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

    if created and faixas_data:
        for faixa in faixas_data:
            Faixa.objects.create(
                album=album,
                titulo=faixa.get('titulo', ''),
                duracao_ms=faixa.get('duracao_ms', 0),
                numero=faixa.get('numero', 1),
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
def listar_albuns(request):
    albuns = Album.objects.all().order_by('-criado_em')
    serializer = AlbumSerializer(albuns, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


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
    return Response(serializer.data, status=status.HTTP_200_OK)


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


# --- Busca local ---

@api_view(['GET'])
def busca(request):
    query = request.query_params.get('q', '')
    if not query:
        return Response({"musicas": [], "albuns": []}, status=status.HTTP_200_OK)

    musicas = Musica.objects.filter(
        Q(titulo__icontains=query) | Q(artista__icontains=query) | Q(genero__icontains=query)
    )
    albuns = Album.objects.filter(
        Q(titulo__icontains=query) | Q(artista__icontains=query) | Q(genero__icontains=query)
    )

    return Response({
        "musicas": MusicaSerializer(musicas, many=True).data,
        "albuns": AlbumSerializer(albuns, many=True).data,
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def react_musica(request, musica_id):
    musica = get_object_or_404(Musica, pk=musica_id)
    action = request.data.get('action')

    if action == 'like':
        musica.likes += 1
    elif action == 'dislike':
        musica.dislikes += 1
    else:
        return Response({'error': 'Ação inválida'}, status=status.HTTP_400_BAD_REQUEST)

    musica.save(update_fields=['likes', 'dislikes'])
    return Response(MusicaSerializer(musica).data, status=status.HTTP_200_OK)


@api_view(['POST'])
def react_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    action = request.data.get('action')

    if action == 'like':
        album.likes += 1
    elif action == 'dislike':
        album.dislikes += 1
    else:
        return Response({'error': 'Ação inválida'}, status=status.HTTP_400_BAD_REQUEST)

    album.save(update_fields=['likes', 'dislikes'])
    return Response(AlbumSerializer(album).data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def reviews_musica(request, musica_id):
    musica = get_object_or_404(Musica, pk=musica_id)

    if request.method == 'GET':
        reviews = Review.objects.filter(musica=musica)
        return Response(ReviewSerializer(reviews, many=True).data, status=status.HTTP_200_OK)

    texto = request.data.get('texto', '').strip()
    autor_nome = request.data.get('autor_nome', '').strip()
    usuario_id = request.data.get('usuario_id')

    if not texto or not autor_nome:
        return Response({'error': 'texto e autor_nome são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)

    review = Review.objects.create(
        musica=musica,
        texto=texto,
        autor_nome=autor_nome,
        usuario_id=usuario_id or None,
    )
    return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def reviews_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)

    if request.method == 'GET':
        reviews = Review.objects.filter(album=album)
        return Response(ReviewSerializer(reviews, many=True).data, status=status.HTTP_200_OK)

    texto = request.data.get('texto', '').strip()
    autor_nome = request.data.get('autor_nome', '').strip()
    usuario_id = request.data.get('usuario_id')

    if not texto or not autor_nome:
        return Response({'error': 'texto e autor_nome são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)

    review = Review.objects.create(
        album=album,
        texto=texto,
        autor_nome=autor_nome,
        usuario_id=usuario_id or None,
    )
    return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def review_reaction(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    action = request.data.get('action')

    if action == 'like':
        review.likes += 1
    elif action == 'dislike':
        review.dislikes += 1
    else:
        return Response({'error': 'Ação inválida'}, status=status.HTTP_400_BAD_REQUEST)

    review.save(update_fields=['likes', 'dislikes'])
    return Response(ReviewSerializer(review).data, status=status.HTTP_200_OK)