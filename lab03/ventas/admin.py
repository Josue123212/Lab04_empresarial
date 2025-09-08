from django.contrib import admin
from .models import (
    Direccion,
    TelefonoCliente,
    Categoria,
    Proveedor,
    Cliente,
    Producto,
    Venta,
    DetalleVenta
)

# Configuración personalizada del Admin

# Inlines para edición relacionada
class TelefonoClienteInline(admin.TabularInline):
    model = TelefonoCliente
    extra = 1  # Mostrar 1 formulario vacío adicional
    max_num = 5  # Máximo 5 teléfonos por cliente
    fields = ('numero',)
    verbose_name = "Teléfono"
    verbose_name_plural = "Teléfonos"

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1  # Mostrar 1 formulario vacío adicional
    max_num = 20  # Máximo 20 productos por venta
    fields = ('producto', 'precio_momento', 'cantidad', 'monto_total')
    readonly_fields = ('monto_total',)  # Campo calculado automáticamente
    verbose_name = "Detalle de Venta"
    verbose_name_plural = "Detalles de Venta"

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('calle', 'numero', 'comuna', 'ciudad')
    search_fields = ('calle', 'comuna', 'ciudad')
    list_filter = ('comuna', 'ciudad')
    fieldsets = (
        ('Información de Dirección', {
            'fields': ('calle', 'numero', 'comuna', 'ciudad')
        }),
    )

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    fieldsets = (
        ('Información de Categoría', {
            'fields': ('nombre', 'descripcion')
        }),
    )

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'telefono', 'direccion')
    search_fields = ('codigo', 'nombre', 'telefono')
    list_filter = ('direccion__ciudad',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre')
        }),
        ('Contacto', {
            'fields': ('telefono', 'web', 'direccion')
        }),
    )

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'direccion')
    search_fields = ('codigo', 'nombre')
    list_filter = ('direccion__ciudad',)
    inlines = [TelefonoClienteInline]  # Agregar inline para teléfonos
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('codigo', 'nombre', 'direccion')
        }),
    )

@admin.register(TelefonoCliente)
class TelefonoClienteAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'numero')
    search_fields = ('cliente__nombre', 'numero')
    list_filter = ('cliente',)
    fieldsets = (
        ('Información de Teléfono', {
            'fields': ('cliente', 'numero')
        }),
    )

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'categoria')
    search_fields = ('nombre',)
    list_filter = ('categoria', 'proveedores')
    filter_horizontal = ('proveedores',)
    fieldsets = (
        ('Información del Producto', {
            'fields': ('nombre', 'categoria')
        }),
        ('Precio y Stock', {
            'fields': ('precio', 'stock')
        }),
        ('Proveedores', {
            'fields': ('proveedores',)
        }),
    )

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'fecha', 'cliente', 'descuento', 'monto')
    search_fields = ('numero_factura', 'cliente__nombre')
    list_filter = ('fecha', 'cliente')
    date_hierarchy = 'fecha'
    inlines = [DetalleVentaInline]  # Agregar inline para detalles de venta
    fieldsets = (
        ('Información de Venta', {
            'fields': ('numero_factura', 'cliente')
        }),
        ('Detalles Financieros', {
            'fields': ('descuento', 'monto')
        }),
    )

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('venta', 'producto', 'precio_momento', 'cantidad', 'monto_total')
    search_fields = ('venta__numero_factura', 'producto__nombre')
    list_filter = ('venta', 'producto')
    fieldsets = (
        ('Información del Detalle', {
            'fields': ('venta', 'producto')
        }),
        ('Detalles de Venta', {
            'fields': ('precio_momento', 'cantidad', 'monto_total')
        }),
    )
