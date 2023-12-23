from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Product
from .forms import ProductCreationForm
from django.urls import reverse_lazy


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    template_name = 'store/add_product.html'
    form_class = ProductCreationForm  

    # Define a custom test function to check if the user 
    def test_func(self):
        return self.request.user.profile.role == 'Super Admin'
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        context['page_title'] = 'Add Product'
        return context

    def form_valid(self, form):
        # Check if a School with the same name already exists
        product_name = form.cleaned_data['name'] 
        if Product.objects.filter(name=product_name).exists():
            messages.error(self.request, 'Product with this name already exists.')
            return self.form_invalid(form)
    
        # Set the added_by field to the logged-in user before saving
        form.instance.added_by = self.request.user
        form.save()

        # Save the form and add a success message
        form.save()
        messages.success(self.request, 'Product Added Successfully.')
        return super().form_valid(form)

    success_url = reverse_lazy('product_list')


class ProductListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    paginate_by = 5

    # function to check if the user is a superuser
    def test_func(self):
        return self.request.user.profile.role == 'Super Admin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        context['page_title'] = 'List of Products'
        return context


# Delete School View
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'store/confirm_product_delete.html'
    success_url = '/product/list/'
    context_object_name = 'product'  # the context object name

    # Define a custom test function to check if the user is a superuser
    def test_func(self):
        return self.request.user.profile.role == 'Super Admin'

    def delete(self, request, *args, **kwargs):
        messages.error(request, 'Product Deleted successfully.')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        context['page_title'] = 'Delete Product'
        return context


# Update School view
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'store/add_product.html'
    form_class = ProductCreationForm  # Use the form for updating

    # Define a custom test function to check if the user is a superuser
    def test_func(self):
        return self.request.user.profile.role == 'Super Admin'

    def form_valid(self, form):
        # Save the form and add a success message
        form.save()
        messages.success(self.request, 'Product Update Successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        context['page_title'] = 'Update Product'
        return context

    success_url = reverse_lazy('product_list')