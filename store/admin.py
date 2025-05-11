from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Product, Order, Cart

# Personnalisation de l'admin pour Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    list_filter = ('stock', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'slug', 'description', 'price', 'stock')
        }),
        ('Média', {
            'fields': ('thumbnail',)
        }),
        ('Dates', {
            'fields': ('created_at',)
        }),
    )

# Personnalisation de l'admin pour Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'ordered', 'ordered_date')
    list_filter = ('ordered', 'ordered_date')
    search_fields = ('user__username', 'product__name')
    ordering = ('-ordered_date',)
    readonly_fields = ('ordered_date',)

    fieldsets = (
        ('Informations de commande', {
            'fields': ('user', 'product', 'quantity', 'ordered')
        }),
        ('Dates', {
            'fields': ('ordered_date',)
        }),
    )

# Personnalisation de l'admin pour Cart
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_orders')
    list_filter = ('user',)
    search_fields = ('user__username',)
    readonly_fields = ('total_orders',)

    def total_orders(self, obj):
        return obj.orders.count()
    total_orders.short_description = 'Nombre de commandes'

# Personnalisation de l'admin pour User
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'last_login')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-last_login',)

    fieldsets = (
        ('Informations de base', {
            'fields': ('username', 'password')
        }),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )

# Inscription des modèles avec leurs configurations personnalisées
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
# Inscription du UserAdmin personnalisé
admin.site.register(User, UserAdmin)
