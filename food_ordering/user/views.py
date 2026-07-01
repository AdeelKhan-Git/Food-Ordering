from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status,permissions
from user.models import User
from user.jwt_token import generated_token
from user.serializer import RegisterSerilizer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class RegisterAPIView(APIView):
    @swagger_auto_schema(
            request_body=RegisterSerilizer,
            responses={201: RegisterSerilizer}
    )
    def post(self,request):
        try:
            serializer =  RegisterSerilizer(data= request.data)
            serializer.is_valid(raise_exception=True)
            validate_data = serializer.validated_data.copy()
            validate_data.pop('confirm_password')

            user = User.objects.create_user(**validate_data)

            token = generated_token(user)

            user.save()

            return Response({'token':token,'data':{'id':user.id,'email':user.email,'username':user.username,
                                        'is_admin':user.is_superuser},'message':'User Resgitered Successfully'},
                                        status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    @swagger_auto_schema(
            request_body=LoginSerializer,
            responses={200: LoginSerializer}
    )
    def post(self,request):
        try:
            serializer = LoginSerializer(data =request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            user = authenticate(email=email, password=password)
            if user is None:
                return Response({'error':'User not Found'}, status= status.HTTP_404_NOT_FOUND)
            
            token = generated_token(user)

            if user.is_superuser == True:

                return Response({'token':token,
                                 'data':{'id':user.id,'email':user.email,'username':user.username,
                                        'is_admin':user.is_superuser},
                                        'message':"User Logged In"}, status= status.HTTP_200_OK)
            else:
                return Response({'token':token,
                                'data':{'id':user.id,'email':user.email,'username':user.username,
                                        'is_admin':user.is_superuser}, 
                                        'message':"User Logged In"}, status= status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)