from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    # username = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, data):
        if User.objects.filter(username=data).exists():
            raise serializers.ValidationError('Username already exists')
        return data

    def save(self, **kwargs):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']


        if pw != repeated_pw:
            raise serializers.ValidationError({'error' : 'password dont match'})
        
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(pw)
        account.save()
        return account

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value
    

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password']
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            
            if not user:
                raise serializers.ValidationError('Ungültige Anmeldedaten', code='authorization')
        else:
            raise serializers.ValidationError('E-Mail und Passwort sind erforderlich.', code='authorization')

        data['user'] = user
        return data


    # def validate_email(self, value):
    #     if User.objects.filter(email=value).exists():
    #         return value
    #     raise serializers.ValidationError('Email not exists')
        

    # def validate_password(self, value):
    #     if User.objects.filter(password=value).exists():
    #         return value
    #     raise serializers.ValidationError('Password not exists')

    # def validate(self, attrs):
    #     user = User.objects.filter(email=attrs['email'], password=attrs['password']).exists()
    #     print(user)
    #     if user:
    #         return attrs
    #     raise serializers.ValidationError('User not found')