import pytest
from rest_framework.test import APIClient
from api_rest.models import Usuario
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.hashers import check_password
from api_rest.models import Musica, Review


@pytest.mark.django_db
def test_ping():
    client = APIClient()
    response = client.get('/api/ping/')
    assert response.status_code == 200
    assert response.json() == {"pong": True}


@pytest.mark.django_db
def test_primeiro_usuario_e_admin():
    client = APIClient()
    response = client.post('/api/data/register/', {
        'user_username': 'gabriel',
        'user_email': 'gabriel@teste.com',
        'user_password': 'senha123',
    }, format='json')
    assert response.status_code == 201
    user = Usuario.objects.get(user_username='gabriel')
    assert user.is_admin is True


@pytest.mark.django_db
def test_perfil_usuario_atualiza_dados_e_lista_reviews():
    client = APIClient()
    register_response = client.post('/api/data/register/', {
        'user_username': 'carol',
        'user_email': 'carol@teste.com',
        'user_password': 'senha123',
        'user_bio': 'bio inicial',
    }, format='json')

    assert register_response.status_code == 201
    usuario = Usuario.objects.get(user_username='carol')

    musica = Musica.objects.create(
        titulo='Musica teste',
        artista='Artista teste',
        spotify_id='spotify-test-001',
    )
    Review.objects.create(
        usuario=usuario,
        autor_nome=usuario.user_username,
        musica=musica,
        texto='Minha primeira review',
    )

    avatar = SimpleUploadedFile('avatar.png', b'fake-image-bytes', content_type='image/png')
    update_response = client.put(
        f'/api/users/{usuario.pk}/perfil/',
        {
            'user_username': 'carol atualizada',
            'user_bio': 'bio atualizada',
            'user_password': 'nova-senha',
            'user_avatar': avatar,
        },
        format='multipart',
    )

    assert update_response.status_code == 200
    usuario.refresh_from_db()
    assert usuario.user_username == 'carol atualizada'
    assert usuario.user_bio == 'bio atualizada'
    assert check_password('nova-senha', usuario.user_password)
    assert usuario.user_avatar.name.startswith('avatars/')

    profile_response = client.get(f'/api/users/{usuario.pk}/perfil/')
    assert profile_response.status_code == 200
    payload = profile_response.json()
    assert payload['review_count'] == 1
    assert payload['reviews'][0]['alvo_titulo'] == 'Musica teste'
    assert payload['reviews'][0]['alvo_tipo'] == 'musica'


@pytest.mark.django_db
def test_review_sem_texto_retorna_400():
    client = APIClient()
    musica = Musica.objects.create(
        titulo='Teste', artista='Artista', spotify_id='sp-val-001'
    )
    response = client.post(
        f'/api/reviews/musicas/{musica.id}/',
        {'texto': '', 'autor_nome': 'usuario', 'nota': 3},
        format='json',
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_review_com_nota_invalida_retorna_400():
    client = APIClient()
    musica = Musica.objects.create(
        titulo='Teste', artista='Artista', spotify_id='sp-val-002'
    )
    response = client.post(
        f'/api/reviews/musicas/{musica.id}/',
        {'texto': 'Boa musica', 'autor_nome': 'usuario', 'nota': 10},
        format='json',
    )
    assert response.status_code == 400
