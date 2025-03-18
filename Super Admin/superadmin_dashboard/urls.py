from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet
from centers.views import CenterViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'centers', CenterViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
]