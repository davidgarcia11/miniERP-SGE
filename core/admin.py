from django.contrib import admin
from .models import Cliente, Estado, Producto

# Configuración básica para el buscador de productos
class ProductoAdmin(admin.ModelAdmin):
    search_fields = ['nombre'] # Esto permite que el autocomplete funcione si lo activas en Ventas

admin.site.register(Cliente)
admin.site.register(Estado)
admin.site.register(Producto, ProductoAdmin)