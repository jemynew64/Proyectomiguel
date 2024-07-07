from rest_framework import serializers
from .models import Product, Cart, CartItem
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

class RegisterSerializer(serializers.ModelSerializer):
    #validando el email si esta bien echo
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    #validando el password
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
        #validando el password2 que sea identico que el 1 
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    #metodo se llama automáticamente durante el proceso de validación del serializador
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        #aca maneja el hashin de la contraseña y le pone un password al objeto
        user.set_password(validated_data['password'])
        user.save()
        return user