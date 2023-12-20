from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.db.models import Q
from .forms import (SuperAdminUserCreationForm,
                    CashierUserCreationForm,
                    PasswordChangeForm
                    )
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# 404 Error Page.
def custom_page_not_found(request, exception=None):
    return render(request, 'accounts/404.html', status=404)


# 403 Error Page.
def custom_page_forbidden(request, exception=None):
    return render(request, 'accounts/403.html', status=403)


# 500 Error Page.
def custom_server_not_found(request, exception=None):
    return render(request, 'accounts/500.html', status=500)


# Dashboard Index
@login_required(login_url='accounts_login')
def index(request):
    logged_user = request.user
    role = logged_user.profile.role
    # Check if logged user account is disabled and redirect
    try:
        active_user = logged_user.profile.is_active
        if not active_user:
            messages.warning(request, f'{logged_user.profile.role} Account is Disabled.')
            return redirect('accounts_login')
    except Profile.DoesNotExist:
        profile = None

    # Get the user's profile
    try:
        profile = logged_user.profile
    except Profile.DoesNotExist:
        profile = None
    # Check if profile exist and user role is Super Admin
    if profile and profile.role == 'Super Admin':
        messages.success(request, f'Welcome Back {role}!')
        return redirect('admin_dashbord')
    # Check if profile exist and user role is Cashier
    elif profile and profile.role == 'Cashier':
        messages.success(request, f'Welcome Back {role}!')
        return redirect('cashier_dashbord')
    # Check if profile exist and user role is Customer
    elif profile and profile.role == 'Customer':
        messages.success(request, f'Welcome Back {role}!')
        return redirect('customer_dashbord')
    else:
        messages.warning(request, 'Something Went Wrong')
        return redirect('accounts_login')


# Admin Dashboard view
def admin_account_dashboard(request):
    logged_user = request.user
    role = logged_user.profile.role
    context = {
        'page_title': f'{role} Dashboard',
    }
    return render(request, 'accounts/index.html', context)


# Cashier Dashboard view
def cashier_account_dashboard(request):
    logged_user = request.user
    role = logged_user.profile.role
    context = {
        'page_title': f'{role} Dashboard',
    }
    return render(request, 'accounts/index.html', context)


# Customer Dashboard view
def customer_account_dashboard(request):
    logged_user = request.user
    role = logged_user.profile.role
    context = {
        'page_title': f'{role} Dashboard',
    }
    return render(request, 'accounts/index.html', context)
    

# Create Super Admin Portal User
@login_required(login_url='accounts_login')
def create_portal_user(request):
    logged_user = request.user
    try:
        user_profile = Profile.objects.get(user=logged_user)
        user_role = user_profile.role
        # Check if logged in user is super admin or admin else don't allow access
        if logged_user.is_superuser:
            if request.method == 'POST':
                form = SuperAdminUserCreationForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    role = form.cleaned_data.get('role')
                    # Get or create the user's profile and update the role
                    profile, created = Profile.objects.get_or_create(user=user)
                    profile.role = role
                    profile.save()
                    
                    messages.success(request, f'{role} Created Successfully.')
            else:
                form = SuperAdminUserCreationForm()
            context = {
                'page_title': 'Create Admin User',
                'form': form
                }
            return render(request, 'accounts/create_super_admin_user.html', context)
        else:
            return redirect('accounts_dashboard')
    except Profile.DoesNotExist:
        # Handle the case when the profile doesn't exist
        return redirect('accounts_dashboard')


# Create Cashier User
@login_required(login_url='accounts_login')
def create_cashier_user(request):
    logged_user = request.user
    try:
        user_profile = Profile.objects.get(user=logged_user)
        user_role = user_profile.role
        # Check if logged in user is super admin or admin else don't allow access
        if logged_user.profile.role == 'Super Admin':
            if request.method == 'POST':
                form = CashierUserCreationForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    role = form.cleaned_data.get('role')
                    # Get or create the user's profile and update the role
                    profile, created = Profile.objects.get_or_create(user=user)
                    profile.role = role
                    profile.save()
                    
                    messages.success(request, f'{role} Created Successfully.')
            else:
                form = CashierUserCreationForm()
            context = {
                'page_title': 'Create Cashier User',
                'form': form
                }
            return render(request, 'accounts/create_super_admin_user.html', context)
        else:
            return redirect('accounts_dashboard')
    except Profile.DoesNotExist:
        # Handle the case when the profile doesn't exist
        return redirect('accounts_dashboard')


@login_required(login_url='accounts_login')
def staff_list(request):
    if request.user.is_superuser or request.user.profile.role in ['Super Admin']:
        # List of Staff
        staff_list = Profile.objects.filter(Q(role="Cashier") | Q(role="Super Admin")).order_by('-last_updated')
        number_of_staff = staff_list.count()

    paginator = Paginator(staff_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_title': 'List of Staff',
        'staff_list': page_obj,
        'number_of_staff': number_of_staff,
    }
    return render(request, 'accounts/staff_list.html', context)


# Disable user
@login_required(login_url='accounts_login')
def disable_user(request, pk):
    if request.user.is_superuser or request.user.profile.role in ['Super Admin']:
        user_to_disable = get_object_or_404(Profile, pk=pk)
        # Change the USER is_active to False
        user_to_disable.is_active = False
        user_to_disable.save()
        messages.error(request, f'{user_to_disable.user.username} Disabled Successfully.')
        return redirect('accounts_staff_list')


# Enable User
@login_required(login_url='accounts_login')
def enable_user(request, pk):
    if request.user.is_superuser or request.user.profile.role in ['Super Admin']:
        user_to_enable = get_object_or_404(Profile, pk=pk)
        # Change the USER is_active to False
        user_to_enable.is_active = True
        user_to_enable.save()
        messages.success(request, f'{user_to_enable.user.username} Enabled Successfully.')
        return redirect('accounts_staff_list')


# Change user password view
@login_required(login_url='accounts_login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.user.username, password=form.cleaned_data['old_password'])
            if user is not None:
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)  # Update session to prevent logout
                messages.success(request, 'Your Password Changed Successfully.')
                return redirect('accounts-password-change-done')  # Redirect to password change success page
            else:
                form.add_error('old_password', 'Incorrect old password')
                messages.warning(request, 'Incorrect old Password.')
    else:
        form = PasswordChangeForm()

    context = {
        'form': form,
        'page_title': 'Change Password',
        }
    return render(request, 'accounts/password_change.html', context)


# Change user password successfully view
@login_required(login_url='accounts_login')
def password_change_done(request):

    context = {
        'page_title': 'Password Changed',
    }
    return render(request, 'accounts/password_change_done.html', context)


# Delete Staff View
class StaffDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'accounts/confirm_delete_staff.html'
    success_url = '/list/portal/users/'
    context_object_name = 'staff'  # the context object name

    # Define a custom test function to check if the user is a superuser
    def test_func(self):
        return self.request.user.profile.role == 'Super Admin'

    def delete(self, request, *args, **kwargs):
        messages.error(request, 'Staff Deleted successfully.')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        context['page_title'] = 'Delete Staff'
        return context