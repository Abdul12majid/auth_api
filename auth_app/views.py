from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, MySerializer, SignupSerializer, PasswordSerializer, AuthSerializer, TokenSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from rest_framework import status

# Create your views here.
@api_view(['GET'])
def home(request):
	if request.user.is_authenticated:
		return Response(f'Welcome {request.user.username}')
	else:
		return Response(f'Hey Stranger')

@api_view(['POST', 'GET'])
def signup(request):
	serializer=UserSerializer(data=request.data)
	if serializer.is_valid():
		current_user=User.objects.filter(username=request.data['username']).first()
		if not current_user:
			serializer.save()
			user=User.objects.get(username=request.data['username'])
			user.set_password(request.data['password'])
			token=Token.objects.create(user=user)
			user.save()
			return Response({'token':token.key, 'user':serializer.data})
		else:
			return Response('Username exists, pick another')
	else:
		return Response("Sign up")

@api_view(['POST','GET'])
def login_user(request):
	serializer=MySerializer(data=request.data)
	if serializer.is_valid():
		username=request.data['username']
		password=request.data['password']
		user=User.objects.filter(username=username).first()
		if not user:
			return Response('Username not found')
		else:
			if not user.check_password(password):
				return Response('Incorrect Password')
			else:
				token, created = Token.objects.get_or_create(user=user)
				current_user=authenticate(request, username=username, password=password)
				if current_user is not None:
					login(request, current_user)
					return Response({'token':token.key, 'user':serializer.data, 'detail':f'welcome {request.user.username}'})
				else:
					return Response({'detail':"User Not found"}, status=status.HTTP_404_NOT_FOUND)
	else:
		return Response({'Info':'Login Below'})


@api_view(['POST', 'GET'])
def signup2(request):
	serializer=SignupSerializer(data=request.data)
	if serializer.is_valid():
		first_name=request.data['first_name']
		last_name=request.data['last_name']
		username=request.data['username']
		password=request.data['password']
		email=request.data['email']
		user=User.objects.filter(username=username).exists()
		if user is True:
			return Response('Username exists, pick another')
		else:
			current_user=User.objects.create_user(
				first_name=first_name, 
				last_name=last_name, 
				username=username, 
				email=email, 
				password=password
				)
			current_user.save()
			user_token=User.objects.get(username=request.data['username'])
			user_token.set_password(request.data['password'])
			token=Token.objects.create(user=user_token)
			user_token.save()
			return Response({'info':'Registration successful', 'token':token.key, 'user':serializer.data})
	else:
		return Response({'Info':'Signup Below'})


@api_view(['POST', 'GET'])
def change_password(request):
	if request.user.is_authenticated:	
		serializer=PasswordSerializer(data=request.data)
		if serializer.is_valid():
			old_password=request.data['old_password']
			new_password=request.data['new_password']
			confirm_password=request.data['confirm_password']
			user=User.objects.get(username=request.user.username)
			if not user.check_password(old_password):
				return Response("Old password incorrect, please correct to change.")
			elif new_password != confirm_password:
				return Response("Password do not match, try again.")
			else:
				user.set_password(request.data['confirm_password'])
				user.save()
				return Response({f'Password changed for {request.user.username}':'successful', 'data':serializer.data})
		else:
			return Response({'Info':'Change password Below'})
	else:
		return Response({'Info':'KIndly log in to change password.'})

@api_view(['POST', 'GET'])
def login_auth(request):
	if request.user.is_authenticated:
		serializer=AuthSerializer(data=request.data)
		get_token=Token.objects.get(user=request.user.username)
		return Response({'info': get_token})
		

		
@api_view(['POST', 'GET'])
def get_all(request):
	get_token=Token.objects.all()
	serializer=TokenSerializer(get_token, many=True)
	return Response(serializer.data)




