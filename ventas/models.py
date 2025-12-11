from django.db import models
from core.models import Cliente, Producto, Estado

def get_estado_borrador():
    """Obtener el estado BORRADOR por defecto"""
    estado, _ = Estado.objects.get_or_create(codigo='BORRADOR', defaults={'nombre': 'Borrador'})
    return estado.id

class Pedido(models.Model):
    """Cabecera del documento de venta"""
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Foreign Keys
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pedidos')
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, related_name='pedidos', default=get_estado_borrador)
    
    # Datos Snapshot (congelados en el tiempo)
    direccion_envio = models.CharField(max_length=250)
    
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"
    
    @property
    def total(self):
        # Suma el total de todas las lineas hijas
        return sum(linea.subtotal for linea in self.lineas.all())

class LineaPedido(models.Model):
    """Filas de detalle del pedido"""
    # Foreign Keys
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='lineas')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    
    # Datos de la línea
    cantidad = models.PositiveIntegerField(default=1)
    
    # Datos Snapshot (Precio al momento de la venta, por si cambia el Producto después)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="% Descuento")
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(cantidad__gt=0),
                name='cantidad_positiva'
            )
        ]
    
    def __str__(self):
        # Cambiamos esto para que muestre el NOMBRE del producto, no solo el SKU
        return f"{self.cantidad}x {self.producto.nombre} ({self.producto.sku})"
    
    @property
    def subtotal(self):
        bruto = self.cantidad * self.precio_unitario
        neto = bruto * (1 - (self.descuento / 100))
        return neto