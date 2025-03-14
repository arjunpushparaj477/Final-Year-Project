from django.urls import path
from .views import CustomLoginView, HomeView, custom_logout

app_name = 'authentication'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
]