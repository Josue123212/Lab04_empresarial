from django.db import models

# Create your models here.

class Direccion(models.Model):
    """
    Modelo para almacenar direcciones de clientes y proveedores
    """
    calle = models.CharField(max_length=200, help_text="Nombre de la calle")
    numero = models.CharField(max_length=10, help_text="Número de la dirección")
    comuna = models.CharField(max_length=100, help_text="Comuna")
    ciudad = models.CharField(max_length=100, help_text="Ciudad")
    
    def __str__(self):
        return f"{self.calle} {self.numero}, {self.comuna}, {self.ciudad}"
    
    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"


class TelefonoCliente(models.Model):
    """
    Modelo para almacenar múltiples teléfonos de un cliente
    """
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, help_text="Cliente propietario del teléfono")
    numero = models.CharField(max_length=15, help_text="Número de teléfono")
    
    def __str__(self):
        return f"{self.cliente.nombre} - {self.numero}"
    
    class Meta:
        verbose_name = "Teléfono de Cliente"
        verbose_name_plural = "Teléfonos de Clientes"


class Categoria(models.Model):
    """
    Modelo para categorizar productos
    """
    nombre = models.CharField(max_length=50, help_text="Nombre de la categoría")
    descripcion = models.TextField(blank=True, help_text="Descripción de la categoría")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


class Proveedor(models.Model):
    """
    Modelo para almacenar información de proveedores
    """
    codigo = models.CharField(max_length=10, unique=True, help_text="Código único del proveedor")
    nombre = models.CharField(max_length=100, help_text="Nombre del proveedor")
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, help_text="Dirección del proveedor")
    telefono = models.CharField(max_length=15, help_text="Teléfono del proveedor")
    web = models.URLField(blank=True, help_text="Página web del proveedor")
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"


class Cliente(models.Model):
    """
    Modelo para almacenar información de clientes
    """
    codigo = models.CharField(max_length=10, unique=True, help_text="Código único del cliente")
    nombre = models.CharField(max_length=100, help_text="Nombre del cliente")
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, help_text="Dirección del cliente")
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Producto(models.Model):
    """
    Modelo para almacenar información de productos
    """
    nombre = models.CharField(max_length=100, help_text="Nombre del producto")
    precio = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio actual del producto")
    stock = models.IntegerField(help_text="Cantidad disponible en inventario")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, help_text="Categoría del producto")
    proveedores = models.ManyToManyField(Proveedor, help_text="Proveedores que suministran este producto")
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class Venta(models.Model):
    """
    Modelo para almacenar información de ventas/facturas
    """
    numero_factura = models.CharField(max_length=20, unique=True, help_text="Número único de factura")
    fecha = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de la venta")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, help_text="Cliente que realiza la compra")
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Descuento aplicado en porcentaje")
    monto = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monto total de la venta")
    
    def calcular_monto_total(self):
        """Calcula el monto total basado en los detalles de venta"""
        from decimal import Decimal
        subtotal = sum(detalle.monto_total for detalle in self.detalleventa_set.all())
        descuento_aplicado = subtotal * (self.descuento / Decimal('100'))
        return subtotal - descuento_aplicado
    
    def actualizar_monto(self):
        """Actualiza el monto de la venta basado en los detalles"""
        self.monto = self.calcular_monto_total()
        self.save()
    
    def __str__(self):
        return f"Factura {self.numero_factura} - {self.cliente.nombre}"
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"


class DetalleVenta(models.Model):
    """
    Modelo para almacenar el detalle de productos en cada venta
    Actúa como tabla intermedia entre Venta y Producto con información adicional
    """
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, help_text="Venta a la que pertenece este detalle")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, help_text="Producto vendido")
    precio_momento = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio del producto al momento de la venta")
    cantidad = models.IntegerField(help_text="Cantidad de productos vendidos")
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monto total de esta línea (precio_momento * cantidad)")
    
    def save(self, *args, **kwargs):
        """Calcula automáticamente el monto_total antes de guardar"""
        self.monto_total = self.precio_momento * self.cantidad
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.venta.numero_factura} - {self.producto.nombre} (x{self.cantidad})"
    
    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Ventas"
