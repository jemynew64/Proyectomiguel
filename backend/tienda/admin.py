from django.contrib import admin
from .models import UserProfile,User,Cart,CartItem,Category,Product
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Category)
admin.site.register(Product)
