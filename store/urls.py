from django.urls import path
from . import views
from .views import (ProductCreateView,
                    ProductListView,
                    ProductDeleteView,
                    ProductUpdateView
                    )


urlpatterns = [
    path('add/product/', ProductCreateView.as_view(), name='add_product'),
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('delete/product/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('update/product/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
]