from django.urls import path, include

from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'perfil', UserProfileViewSet)
router.register(r'categoria', CategoryViewSet)
router.register(r'producto', ProductViewSet)
router.register(r'carrito', CartViewSet)
router.register(r'carritoitem', CartItemViewSet)

urlpatterns = [
      path('', include(router.urls)),
]
