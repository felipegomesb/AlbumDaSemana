from rest_framework import serializers
from .models import Usuario



class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        #id with uuid4
        fields = ['id', 'user_username', 'user_email', 'user_password']

