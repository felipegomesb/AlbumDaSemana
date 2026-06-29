from django.urls import path
from . import views


urlpatterns = [
    # Usuários
    path('users/', views.get_users, name='get_users'),
    path('users/<str:username>/', views.get_user_by_username, name='get_user_by_username'),
    path('users/<int:pk>/', views.get_user_by_pk, name='get_user_by_pk'),
    path('data/', views.user_manager, name='user_manager'),
    path('data/login/', views.login, name='user_login'),
    path('data/register/', views.register, name='user_register'),

    # Spotify
    path('spotify/search/', views.spotify_search, name='spotify_search'),
    path('spotify/add-track/', views.spotify_add_track, name='spotify_add_track'),
    path('spotify/add-album/', views.spotify_add_album, name='spotify_add_album'),

    # Catálogo local
    path('musicas/', views.listar_musicas, name='listar_musicas'),
    path('albuns/', views.listar_albuns, name='listar_albuns'),

    # Rotação automática
    path('musica-do-dia/', views.musica_do_dia, name='musica_do_dia'),
    path('album-da-semana/', views.album_da_semana, name='album_da_semana'),

    # Histórico
    path('historico/musicas/', views.historico_musicas, name='historico_musicas'),
    path('historico/albuns/', views.historico_albuns, name='historico_albuns'),

    # Busca
    path('busca/', views.busca, name='busca'),

    # Reviews
    path('reviews/musicas/<int:musica_id>/', views.reviews_musica, name='reviews_musica'),
    path('reviews/albuns/<int:album_id>/', views.reviews_album, name='reviews_album'),
    path('reviews/<int:review_id>/reaction/', views.review_reaction, name='review_reaction'),

    # Ping
    path('ping/', views.ping, name='ping'),
]
