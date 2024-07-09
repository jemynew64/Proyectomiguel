#si no estoy mal es un metodo de signals para despues de un guardado mirar la documentacion
from django.db.models.signals import post_save, pre_save, post_delete
#este es porque use el modelo del user del mismo django
from django.contrib.auth.models import User
#importar los modelos que usare 
from .models import *
#manera recomendad decorador para hacer esto de signals
from django.dispatch import receiver

@receiver(post_save, sender = User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        #cuando creo un usuario le creo tambien su coneccion con user profile y su carrito
        UserProfile.objects.create(user = instance)
        Cart.objects.create(user = instance)
        print("se creo un carrito y perfil usuario")
        
# @receiver(post_save, sender = User)
# def create_card(sender,instance,created, **kwargs):
#     if created:
#         Cart.objects.create(user = instance)

#basicamente lo que hago aca es que si digamos habia 20 en stock tenia 10 y le cambie a 30
#esto impediera eso y me mandara un error y no lo dejara hacer solo si excede el stock
@receiver(pre_save, sender=CartItem)
def verificar_stock_antes_de_guardar(sender, instance, **kwargs):
    # Obtener el producto asociado
    product = instance.product
    #obtener mi llave primaria
    if instance.pk:
        # Si es una actualización, obtener el CartItem anterior para ajustar el stock
        previous_item = CartItem.objects.get(pk=instance.pk)
        quantity_difference = instance.quantity - previous_item.quantity
    else:
        # Si es una nueva adición, simplemente usamos la cantidad actual
        quantity_difference = instance.quantity

    # Verificar si hay suficiente stock
    if product.stock < quantity_difference:
        raise ValidationError(f"No hay suficiente stock para {product.name}. Stock disponible: {product.stock}")

@receiver(post_save, sender=CartItem)
def actualizar_stock_despues_de_guardar(sender, instance, created, **kwargs):
    product = instance.product
    if created:
        # Si es una nueva adición, restar la cantidad del stock
        product.stock -= instance.quantity
    else:
        # Si es una actualización, ajustar el stock basado en la diferencia de cantidad
        previous_item = CartItem.objects.get(pk=instance.pk)
        quantity_difference = instance.quantity - previous_item.quantity
        product.stock -= quantity_difference
    product.save()

@receiver(post_delete, sender=CartItem)
def devolver_stock_despues_de_eliminar(sender, instance, **kwargs):
    # Devolver la cantidad del stock cuando se elimina un CartItem
    product = instance.product
    product.stock += instance.quantity
    product.save()
