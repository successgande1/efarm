from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from .views import StaffDeleteView

urlpatterns = [
    path('Login/', auth_view.LoginView.as_view(template_name='accounts/login.html'), name='accounts_login'),
    path('Dashboard/', views.index, name='accounts_dashboard'),
    path('create/super_user/', views.create_portal_user, name='create_portal_user'),
    path('create/cashier_user/', views.create_cashier_user, name='create_cashier_user'),
    path('staff/list/', views.staff_list, name='accounts_staff_list'),
    path('disable_user/<int:pk>/', views.disable_user, name='accounts_disable_user'),
    path('enable_user/<int:pk>/', views.enable_user, name='accounts_enable_user'),
    path('delete/staff/<int:pk>/', StaffDeleteView.as_view(), name='delete_staff'),
    path('logout/', auth_view.LogoutView.as_view(template_name='accounts/logout.html'), name='accounts_logout'),
]