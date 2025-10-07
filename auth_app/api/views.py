from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from .serializers import RegistrationSerializer, LoginSerializer


User = get_user_model()

class RegistrationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        fullname = request.data["fullname"].split()
        fullname = "_".join(fullname)
        new_data = {
            "username" : fullname,
            "email" : request.data["email"],
            "password" : request.data["password"],
            "repeated_password" : request.data["repeated_password"]
        }
        
        serializer = RegistrationSerializer(data=new_data)
        
        
        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            saved_account.username = request.data["fullname"]
            data = {
                'token' : token.key,
                'fullname' : saved_account.username,
                'email' : saved_account.email,
                'user_id' : saved_account.id
            }
        else:
            data = serializer.errors
        
        return Response(data)
    

class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "E-Mail ist erforderlich."},
                status=status.HTTP_400_BAD_REQUEST
                )
        user = User.objects.get(email=email)
            
        username = user.username
        print(username)

        request.data["username"] = username
        serializer = self.serializer_class(data=request.data)


        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token' : token.key,
                'fullname' : user.username,
                'email' : user.email,
                'user_id' : user.id
            }
        else:
            data = serializer.errors
        

        return Response(data)