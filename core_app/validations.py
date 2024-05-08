from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status


UserModel = get_user_model()

def custom_validation(data):
    email = data['email'].strip()
    username = data['username'].strip()
    password = data['password'].strip()
    print(email, username, password)
    ##
    if not email or UserModel.objects.filter(email=email).exists():
        return Response('Email is already taken, please choose another one!', status=status.HTTP_400_BAD_REQUEST)
    ##
    if not password or len(password) < 8:
        return Response('Password is too weak! Minimum length should be 8 characters!', status=status.HTTP_400_BAD_REQUEST)
    ##
    if not username:
        return Response('Please choose another username!', status=status.HTTP_400_BAD_REQUEST)
    return data


def validate_email(data):
    email = data['email'].strip()
    if not email:
        raise ValidationError('an email is needed')
    return True

def validate_username(data):
    username = data['username'].strip()
    if not username:
        raise ValidationError('choose another username')
    return True

def validate_password(data):
    password = data['password'].strip()
    if not password:
        raise ValidationError('a password is needed')
    return True
