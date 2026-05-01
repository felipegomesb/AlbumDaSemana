from urllib import request

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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