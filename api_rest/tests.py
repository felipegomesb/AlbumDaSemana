import pytest
from rest_framework.test import APIClient
from api_rest.models import Usuario


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
