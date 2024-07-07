from django.db import models
#para dar errores pesonalizados
from django.core.exceptions import ValidationError
#importando el usuaurio de django
from django.contrib.auth.models import User


#haciendole un usuario modificado por mi sin modificar el original
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con el modelo de usuario predeterminado.
    bio = models.TextField(blank=True)  # Biografía opcional.
    birth_date = models.DateField(null=True, blank=True)  # Fecha de nacimiento opcional.
    location = models.CharField(max_length=100, blank=True)  # Ubicación opcional.
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)  # Foto de perfil opcional.
    
    def __str__(self):
        return self.user.username  # Muestra el nombre de usuario cuando se imprime el perfil.


def validate_positive(value):
    if value <= 0:
        raise ValidationError('%s is not a positive number' % value)

#cuando no les pongo el id se pone por defecto en django

class Category(models.Model):
    name = models.CharField(max_length=255)  # Campo para cadenas de texto, útil para nombres.
    def __str__(self):
        return self.name  
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)  # Campo para cadenas de texto, útil para nombres.
    description = models.TextField()  # Campo para texto más largo, útil para descripciones detalladas.
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Campo para números decimales, útil para precios.}
    ##aca es lo normal pero le agrego validators y le pongo una validacion echa por mi 
    stock = models.IntegerField(validators=[validate_positive])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Campo para relaciones uno a muchos.
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

#tabla intermedia 
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    