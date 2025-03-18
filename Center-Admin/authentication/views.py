from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    
    def get_success_url(self):
        if self.request.user.is_staff or self.request.user.role == 'admin':
            return reverse_lazy('administration:admin_dashboard')
        return reverse_lazy('home')  # or whatever your default redirect should be
    redirect_authenticated_user = True
    
    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.role == 'admin':
            return reverse_lazy('administration:admin_dashboard')
        elif user.role == 'zone_leader':
            return reverse_lazy('administration:zone_dashboard')
        elif user.role == 'cell_leader':
            return reverse_lazy('administration:cell_dashboard')
        return reverse_lazy('authentication:home')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('authentication:home')
