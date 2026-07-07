from django.urls import path
from . import views


urlpatterns = [
    # Usuários
    path('users/', views.get_users, name='get_users'),
    path('users/<str:username>/', views.get_user_by_username, name='get_user_by_username'),
    path('users/<int:pk>/', views.get_user_by_pk, name='get_user_by_pk'),
    path('users/<int:pk>/perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('users/<int:pk>/reviews/', views.user_reviews, name='user_reviews'),
    path('data/', views.user_manager, name='user_manager'),
    path('data/login/', views.login, name='user_login'),
    path('data/register/', views.register, name='user_register'),

    # Spotify
    path('spotify/search/', views.spotify_search, name='spotify_search'),
    path('spotify/add-track/', views.spotify_add_track, name='spotify_add_track'),
    path('spotify/add-album/', views.spotify_add_album, name='spotify_add_album'),

    # Catálogo local
    path('musicas/', views.listar_musicas, name='listar_musicas'),
    path('musicas/<int:musica_id>/', views.detalhe_musica, name='detalhe_musica'),
    path('albuns/', views.listar_albuns, name='listar_albuns'),
    path('albuns/<int:album_id>/', views.detalhe_album, name='detalhe_album'),
    path('musicas/<int:musica_id>/react/', views.react_musica, name='react_musica'),
    path('albuns/<int:album_id>/react/', views.react_album, name='react_album'),

    # Rotação automática
    path('musica-do-dia/', views.musica_do_dia, name='musica_do_dia'),
    path('musica-do-dia/definir/', views.definir_musica_do_dia, name='definir_musica_do_dia'),
    path('album-da-semana/', views.album_da_semana, name='album_da_semana'),
    path('album-da-semana/definir/', views.definir_album_da_semana, name='definir_album_da_semana'),

    # Histórico
    path('historico/musicas/', views.historico_musicas, name='historico_musicas'),
    path('historico/albuns/', views.historico_albuns, name='historico_albuns'),

    # Busca
    path('busca/', views.busca, name='busca'),
    path('busca/spotify/', views.busca_spotify, name='busca_spotify'),

    # Garantir (auto-save do Spotify para o banco local)
    path('musicas/garantir/', views.garantir_musica, name='garantir_musica'),
    path('albuns/garantir/', views.garantir_album, name='garantir_album'),

    # Reviews
    path('reviews/musicas/<int:musica_id>/', views.reviews_musica, name='reviews_musica'),
    path('reviews/albuns/<int:album_id>/', views.reviews_album, name='reviews_album'),
    path('reviews/<int:review_id>/', views.review_detail, name='review_detail'),
    path('reviews/<int:review_id>/reaction/', views.review_reaction, name='review_reaction'),

    # Rankings
    path('rankings/', views.rankings, name='rankings'),

    # Ping
    path('ping/', views.ping, name='ping'),

]
