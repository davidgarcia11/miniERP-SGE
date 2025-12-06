from django.contrib import admin
from .models import Pedido, LineaPedido

# Configuración para editar las líneas DENTRO del pedido
class LineaPedidoInline(admin.TabularInline):
    model = LineaPedido
    extra = 1
    # autocomplete_fields = ['producto'] # Descomenta esto solo si configuras search_fields en ProductoAdmin

# Configuración del Pedido
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_creacion', 'estado', 'total_calculado')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('cliente__nombre', 'id')
    inlines = [LineaPedidoInline] # Esto mete las líneas dentro del pedido

    def total_calculado(self, obj):
        return f"{obj.total} €"
    total_calculado.short_description = "Total"

# Registramos Pedido con su configuración avanzada
admin.site.register(Pedido, PedidoAdmin)

# (Opcional) Si no quieres ver 'Lineas de Pedido' sueltas en el menú, borra la siguiente línea:
admin.site.register(LineaPedido)