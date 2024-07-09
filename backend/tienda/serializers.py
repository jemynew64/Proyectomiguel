from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

class UserProfileSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = UserProfile
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Product
        fields = '__all__'
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        
class CartItemProfileSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = CartItem
        fields = '__all__'

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
        
        # Crear un carrito para el usuario recién creado
        #Cart.objects.create(user=user)

        return user