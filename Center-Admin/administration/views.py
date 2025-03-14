from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Zone, Cell
from authentication.models import CustomUser
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from authentication.models import CustomUser
from authentication.forms import CustomUserCreationForm
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'administration/users/user_form.html'
    success_url = reverse_lazy('administration:user_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'User created successfully!')
        return super().form_valid(form)
from .forms import ZoneForm
from .models import Zone
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Report

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'administration/admin_dashboard.html'
    
    def test_func(self):
        return self.request.user.is_staff or self.request.user.role == 'admin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_users'] = CustomUser.objects.count()
        context['total_zones'] = Zone.objects.count()
        context['total_cells'] = Cell.objects.count()
        context['recent_zones'] = Zone.objects.all().order_by('-created_at')[:5]
        context['recent_cells'] = Cell.objects.all().order_by('-created_at')[:5]
        return context


class ZoneCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Zone
    form_class = ZoneForm
    template_name = 'administration/zones/zone_form.html'
    success_url = reverse_lazy('administration:admin_dashboard')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.role == 'admin'

    def form_valid(self, form):
        messages.success(self.request, 'Zone created successfully!')
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'administration/users/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff

class ZoneListView(LoginRequiredMixin, ListView):
    model = Zone
    template_name = 'administration/zones/zone_list.html'
    context_object_name = 'zones'
    paginate_by = 10

class CellListView(LoginRequiredMixin, ListView):
    model = Cell
    template_name = 'administration/cells/cell_list.html'
    context_object_name = 'cells'
    paginate_by = 10


class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'administration/reports/report_list.html'
    context_object_name = 'reports'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            # Filter reports based on user's role
            if hasattr(self.request.user, 'zone'):
                queryset = queryset.filter(zone=self.request.user.zone)
            elif hasattr(self.request.user, 'cell'):
                queryset = queryset.filter(cell=self.request.user.cell)
        return queryset.select_related('zone', 'cell', 'created_by')


class UserEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'administration/users/user_form.html'
    success_url = reverse_lazy('administration:user_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'User updated successfully!')
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Make password optional in edit mode
        form.fields['password1'].required = False
        form.fields['password2'].required = False
        return form


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = CustomUser
    template_name = 'administration/users/user_confirm_delete.html'
    success_url = reverse_lazy('administration:user_list')
    success_message = "User was deleted successfully."

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
