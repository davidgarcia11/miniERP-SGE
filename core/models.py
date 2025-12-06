from django.db import models

class Cliente(models.Model):
    """Información de quien nos compra"""
    razon_social = models.CharField(max_length=150, verbose_name="Razón Social")
    cif = models.CharField(max_length=20, verbose_name="NIF/CIF")
    nombre_contacto = models.CharField(max_length=100, verbose_name="Persona de contacto")
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=250, verbose_name="Dirección Fiscal")
    
    def __str__(self):
        return self.razon_social

class Estado(models.Model):
    """Estados del ciclo de vida del pedido (Pendiente, Pagado, Enviado...)"""
    nombre = models.CharField(max_length=50)
    orden = models.IntegerField(default=0, help_text="Para ordenar en listas (1, 2, 3...)")

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    """Catálogo de artículos"""
    sku = models.CharField(max_length=20, unique=True, verbose_name="SKU / Ref")
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    
    # Datos económicos
    coste = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Coste Compra")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="PVP Venta")
    iva = models.IntegerField(default=21, choices=[(21, '21%'), (10, '10%'), (4, '4%'), (0, '0%')])
    
    # Stock
    stock = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.sku})"