from django.urls import path
from . import views
from .admin_views import admin_dashboard, product_list, product_add, product_edit, order_list, user_list

app_name = 'store'

urlpatterns = [
    # Pages principales
    path('', views.index, name='index'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/delete/', views.delete_cart, name='delete_cart'),
    
    # Interface admin
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('admin/products/', product_list, name='product_list'),
    path('admin/products/add/', product_add, name='product_add'),
    path('admin/products/<int:product_id>/edit/', product_edit, name='product_edit'),
    path('admin/orders/', order_list, name='order_list'),
    path('admin/users/', user_list, name='user_list'),
]
