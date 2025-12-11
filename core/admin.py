from django.contrib import admin
from .models import Cliente, Producto, Estado

# Configuración básica para el buscador de productos
class ProductoAdmin(admin.ModelAdmin):
    search_fields = ['nombre'] # Esto permite que el autocomplete funcione si lo activas en Ventas

admin.site.register(Cliente)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Estado)