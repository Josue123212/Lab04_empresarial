# ESQUEMA DE CLASES Y MODELOS - SISTEMA DE VENTAS

## 1. DEFINIR EL ESQUEMA DE CLASES Y SUS OBJETOS

### Análisis del Problema

Se requiere diseñar una BD para registrar ventas de una empresa que controle:
- **Proveedores**: Código, nombre, dirección, teléfono, página web
- **Clientes**: Código, nombre, dirección, múltiples teléfonos
- **Productos**: ID, nombre, precio, stock, proveedor, categoría
- **Ventas**: Número factura, fecha, cliente, descuento, monto
- **Direcciones**: Calle, número, comuna, ciudad
- **Categorías**: ID, nombre, descripción

### Esquema de Clases

```
Dirección
├── calle: CharField
├── numero: CharField
├── comuna: CharField
└── ciudad: CharField

Cliente
├── codigo: CharField (único)
├── nombre: CharField
├── direccion: ForeignKey(Dirección)
└── telefonos: OneToMany(TelefonoCliente)

TelefonoCliente
├── cliente: ForeignKey(Cliente)
└── numero: CharField

Proveedor
├── codigo: CharField (único)
├── nombre: CharField
├── direccion: ForeignKey(Dirección)
├── telefono: CharField
└── pagina_web: URLField

Categoría
├── nombre: CharField (único)
└── descripcion: TextField

Producto
├── nombre: CharField
├── precio: DecimalField
├── stock: PositiveIntegerField
├── categoria: ForeignKey(Categoría)
└── proveedores: ManyToMany(Proveedor)

Venta
├── numero_factura: CharField (único)
├── fecha: DateTimeField
├── cliente: ForeignKey(Cliente)
├── descuento: DecimalField
├── monto_total: DecimalField
└── detalles: OneToMany(DetalleVenta)

DetalleVenta
├── venta: ForeignKey(Venta)
├── producto: ForeignKey(Producto)
├── precio_momento: DecimalField
├── cantidad: PositiveIntegerField
└── monto_total: DecimalField
```

### Relaciones Entre Clases

- **Cliente → Dirección**: ForeignKey (PROTECT)
- **Cliente → TelefonoCliente**: OneToMany (CASCADE)
- **Proveedor → Dirección**: ForeignKey (PROTECT)
- **Producto → Categoría**: ForeignKey (PROTECT)
- **Producto ↔ Proveedor**: ManyToMany
- **Venta → Cliente**: ForeignKey (PROTECT)
- **DetalleVenta → Venta**: ForeignKey (CASCADE)
- **DetalleVenta → Producto**: ForeignKey (PROTECT)

## 2. REALIZAR LOS MODELS

### models.py

```python
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Direccion(models.Model):
    calle = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    comuna = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"
    
    def __str__(self):
        return f"{self.calle} {self.numero}, {self.comuna}, {self.ciudad}"

class Cliente(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    direccion = models.ForeignKey(Direccion, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class TelefonoCliente(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='telefonos')
    numero = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = "Teléfono de Cliente"
        verbose_name_plural = "Teléfonos de Clientes"
        unique_together = ['cliente', 'numero']
    
    def __str__(self):
        return f"{self.cliente.nombre} - {self.numero}"

class Proveedor(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    direccion = models.ForeignKey(Direccion, on_delete=models.PROTECT)
    telefono = models.CharField(max_length=20)
    pagina_web = models.URLField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    stock = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    proveedores = models.ManyToManyField(Proveedor)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class Venta(models.Model):
    numero_factura = models.CharField(max_length=50, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, validators=[MinValueValidator(Decimal('0.00'))])
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha']
    
    def calcular_monto_total(self):
        subtotal = sum(detalle.monto_total for detalle in self.detalles.all())
        descuento_aplicado = subtotal * (self.descuento / 100)
        self.monto_total = subtotal - descuento_aplicado
        return self.monto_total
    
    def actualizar_monto(self):
        self.calcular_monto_total()
        self.save()
    
    def __str__(self):
        return f"Factura {self.numero_factura} - {self.cliente.nombre}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    precio_momento = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Venta"
        unique_together = ['venta', 'producto']
    
    def save(self, *args, **kwargs):
        self.monto_total = self.precio_momento * self.cantidad
        super().save(*args, **kwargs)
        self.venta.actualizar_monto()
    
    def __str__(self):
        return f"{self.venta.numero_factura} - {self.producto.nombre} (x{self.cantidad})"
```

## 3. COLOCAR DATOS FICTICIOS

### Script de Población de Datos

```python
from django.core.management.base import BaseCommand
from ventas.models import *
from decimal import Decimal
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Poblar la base de datos con datos ficticios'
    
    def handle(self, *args, **options):
        # Limpiar datos existentes
        DetalleVenta.objects.all().delete()
        Venta.objects.all().delete()
        Producto.objects.all().delete()
        TelefonoCliente.objects.all().delete()
        Cliente.objects.all().delete()
        Proveedor.objects.all().delete()
        Categoria.objects.all().delete()
        Direccion.objects.all().delete()
        
        # Crear Direcciones
        direcciones_data = [
            {"calle": "Av. Libertador", "numero": "1234", "comuna": "Las Condes", "ciudad": "Santiago"},
            {"calle": "Calle Principal", "numero": "567", "comuna": "Providencia", "ciudad": "Santiago"},
            {"calle": "Av. Grecia", "numero": "890", "comuna": "Ñuñoa", "ciudad": "Santiago"},
            {"calle": "Calle Comercio", "numero": "123", "comuna": "Valparaíso", "ciudad": "Valparaíso"},
            {"calle": "Av. Brasil", "numero": "456", "comuna": "Valparaíso", "ciudad": "Valparaíso"},
            {"calle": "Calle Arturo Prat", "numero": "789", "comuna": "Concepción", "ciudad": "Concepción"},
            {"calle": "Av. Colón", "numero": "321", "comuna": "Concepción", "ciudad": "Concepción"},
            {"calle": "Calle Baquedano", "numero": "654", "comuna": "La Serena", "ciudad": "La Serena"},
            {"calle": "Av. Francisco de Aguirre", "numero": "987", "comuna": "La Serena", "ciudad": "La Serena"},
            {"calle": "Calle Zenteno", "numero": "147", "comuna": "Antofagasta", "ciudad": "Antofagasta"}
        ]
        
        direcciones = []
        for data in direcciones_data:
            direccion = Direccion.objects.create(**data)
            direcciones.append(direccion)
            print(f"✅ Dirección creada: {direccion}")
        
        # Crear Categorías
        categorias_data = [
            {"nombre": "Electrónicos", "descripcion": "Dispositivos electrónicos y tecnología"},
            {"nombre": "Ropa", "descripcion": "Vestimenta y accesorios"},
            {"nombre": "Hogar", "descripcion": "Artículos para el hogar"},
            {"nombre": "Deportes", "descripcion": "Equipamiento deportivo"},
            {"nombre": "Libros", "descripcion": "Literatura y material educativo"}
        ]
        
        categorias = []
        for data in categorias_data:
            categoria = Categoria.objects.create(**data)
            categorias.append(categoria)
            print(f"✅ Categoría creada: {categoria}")
        
        # Crear Proveedores
        proveedores_data = [
            {"codigo": "PROV001", "nombre": "TechnoSupply Ltda.", "telefono": "+56912345678", "pagina_web": "https://technosupply.cl"},
            {"codigo": "PROV002", "nombre": "Distribuidora Central", "telefono": "+56987654321", "pagina_web": "https://distcentral.cl"},
            {"codigo": "PROV003", "nombre": "Importadora Global", "telefono": "+56911111111", "pagina_web": "https://impglobal.cl"},
            {"codigo": "PROV004", "nombre": "Textiles del Sur", "telefono": "+56922222222", "pagina_web": "https://textilesdelsur.cl"},
            {"codigo": "PROV005", "nombre": "Hogar y Más", "telefono": "+56933333333", "pagina_web": "https://hogarymas.cl"},
            {"codigo": "PROV006", "nombre": "Deportes Extremos", "telefono": "+56944444444", "pagina_web": "https://deportesextremos.cl"},
            {"codigo": "PROV007", "nombre": "Editorial Conocimiento", "telefono": "+56955555555", "pagina_web": "https://editorialconocimiento.cl"},
            {"codigo": "PROV008", "nombre": "Mega Distribuidora", "telefono": "+56966666666", "pagina_web": "https://megadist.cl"}
        ]
        
        proveedores = []
        for i, data in enumerate(proveedores_data):
            data['direccion'] = direcciones[i % len(direcciones)]
            proveedor = Proveedor.objects.create(**data)
            proveedores.append(proveedor)
            print(f"✅ Proveedor creado: {proveedor}")
        
        # Crear Clientes
        clientes_data = [
            {"codigo": "CLI001", "nombre": "Juan Pérez González"},
            {"codigo": "CLI002", "nombre": "María García López"},
            {"codigo": "CLI003", "nombre": "Carlos Rodríguez Silva"},
            {"codigo": "CLI004", "nombre": "Ana Martínez Torres"},
            {"codigo": "CLI005", "nombre": "Luis Fernández Ruiz"},
            {"codigo": "CLI006", "nombre": "Carmen Sánchez Morales"},
            {"codigo": "CLI007", "nombre": "Roberto Díaz Herrera"},
            {"codigo": "CLI008", "nombre": "Patricia Jiménez Castro"},
            {"codigo": "CLI009", "nombre": "Miguel Vargas Peña"},
            {"codigo": "CLI010", "nombre": "Isabel Romero Vega"},
            {"codigo": "CLI011", "nombre": "Francisco Muñoz Soto"},
            {"codigo": "CLI012", "nombre": "Claudia Herrera Ramos"},
            {"codigo": "CLI013", "nombre": "Andrés Castillo Flores"},
            {"codigo": "CLI014", "nombre": "Mónica Guerrero Mendoza"},
            {"codigo": "CLI015", "nombre": "Ricardo Moreno Aguilar"}
        ]
        
        clientes = []
        for i, data in enumerate(clientes_data):
            data['direccion'] = direcciones[i % len(direcciones)]
            cliente = Cliente.objects.create(**data)
            clientes.append(cliente)
            print(f"✅ Cliente creado: {cliente}")
        
        # Crear Teléfonos de Clientes
        telefonos_data = [
            "+56912345678", "+56987654321", "+56911111111", "+56922222222", "+56933333333",
            "+56944444444", "+56955555555", "+56966666666", "+56977777777", "+56988888888",
            "+56999999999", "+56900000000", "+56911111112", "+56922222223", "+56933333334",
            "+56944444445", "+56955555556", "+56966666667", "+56977777778", "+56988888889",
            "+56999999990", "+56900000001", "+56911111113", "+56922222224", "+56933333335"
        ]
        
        for i, numero in enumerate(telefonos_data):
            cliente = clientes[i % len(clientes)]
            telefono = TelefonoCliente.objects.create(cliente=cliente, numero=numero)
            print(f"✅ Teléfono creado: {telefono}")
        
        # Crear Productos
        productos_data = [
            {"nombre": "Laptop Dell Inspiron", "precio": Decimal('899.99'), "stock": 15, "categoria": categorias[0]},
            {"nombre": "Smartphone Samsung Galaxy", "precio": Decimal('699.99'), "stock": 25, "categoria": categorias[0]},
            {"nombre": "Tablet iPad Air", "precio": Decimal('599.99'), "stock": 12, "categoria": categorias[0]},
            {"nombre": "Auriculares Bluetooth", "precio": Decimal('149.99'), "stock": 30, "categoria": categorias[0]},
            {"nombre": "Monitor 24 pulgadas", "precio": Decimal('299.99'), "stock": 18, "categoria": categorias[0]},
            {"nombre": "Teclado Mecánico", "precio": Decimal('89.99'), "stock": 22, "categoria": categorias[0]},
            {"nombre": "Mouse Inalámbrico", "precio": Decimal('39.99'), "stock": 35, "categoria": categorias[0]},
            {"nombre": "Camiseta Polo", "precio": Decimal('29.99'), "stock": 50, "categoria": categorias[1]},
            {"nombre": "Jeans Clásicos", "precio": Decimal('79.99'), "stock": 40, "categoria": categorias[1]},
            {"nombre": "Chaqueta de Cuero", "precio": Decimal('199.99'), "stock": 15, "categoria": categorias[1]},
            {"nombre": "Zapatos Deportivos", "precio": Decimal('119.99'), "stock": 28, "categoria": categorias[1]},
            {"nombre": "Vestido Elegante", "precio": Decimal('89.99'), "stock": 20, "categoria": categorias[1]},
            {"nombre": "Sofá 3 Plazas", "precio": Decimal('799.99'), "stock": 8, "categoria": categorias[2]},
            {"nombre": "Mesa de Comedor", "precio": Decimal('499.99'), "stock": 12, "categoria": categorias[2]},
            {"nombre": "Lámpara de Pie", "precio": Decimal('129.99'), "stock": 25, "categoria": categorias[2]},
            {"nombre": "Aspiradora Robot", "precio": Decimal('349.99'), "stock": 10, "categoria": categorias[2]},
            {"nombre": "Microondas", "precio": Decimal('199.99'), "stock": 15, "categoria": categorias[2]},
            {"nombre": "Bicicleta Montaña", "precio": Decimal('599.99'), "stock": 12, "categoria": categorias[3]},
            {"nombre": "Pelota de Fútbol", "precio": Decimal('29.99'), "stock": 45, "categoria": categorias[3]},
            {"nombre": "Raqueta de Tenis", "precio": Decimal('149.99'), "stock": 18, "categoria": categorias[3]},
            {"nombre": "Pesas Ajustables", "precio": Decimal('199.99'), "stock": 20, "categoria": categorias[3]},
            {"nombre": "Cinta de Correr", "precio": Decimal('899.99'), "stock": 5, "categoria": categorias[3]},
            {"nombre": "Casco de Ciclismo", "precio": Decimal('79.99'), "stock": 25, "categoria": categorias[3]},
            {"nombre": "El Quijote", "precio": Decimal('19.99'), "stock": 30, "categoria": categorias[4]},
            {"nombre": "Cien Años de Soledad", "precio": Decimal('24.99'), "stock": 25, "categoria": categorias[4]},
            {"nombre": "Manual de Python", "precio": Decimal('49.99'), "stock": 20, "categoria": categorias[4]},
            {"nombre": "Historia de Chile", "precio": Decimal('34.99'), "stock": 15, "categoria": categorias[4]},
            {"nombre": "Diccionario Español", "precio": Decimal('29.99'), "stock": 18, "categoria": categorias[4]},
            {"nombre": "Atlas Mundial", "precio": Decimal('39.99'), "stock": 12, "categoria": categorias[4]},
            {"nombre": "Enciclopedia Infantil", "precio": Decimal('59.99'), "stock": 10, "categoria": categorias[4]}
        ]
        
        productos = []
        for data in productos_data:
            producto = Producto.objects.create(**data)
            # Asignar proveedores aleatorios
            num_proveedores = random.randint(1, 3)
            proveedores_asignados = random.sample(proveedores, num_proveedores)
            producto.proveedores.set(proveedores_asignados)
            productos.append(producto)
            print(f"✅ Producto creado: {producto}")
        
        # Crear Ventas
        ventas_data = [
            {"numero_factura": "FACT-001", "descuento": Decimal('5.00')},
            {"numero_factura": "FACT-002", "descuento": Decimal('0.00')},
            {"numero_factura": "FACT-003", "descuento": Decimal('10.00')},
            {"numero_factura": "FACT-004", "descuento": Decimal('2.50')},
            {"numero_factura": "FACT-005", "descuento": Decimal('0.00')},
            {"numero_factura": "FACT-006", "descuento": Decimal('7.50')},
            {"numero_factura": "FACT-007", "descuento": Decimal('15.00')},
            {"numero_factura": "FACT-008", "descuento": Decimal('0.00')},
            {"numero_factura": "FACT-009", "descuento": Decimal('5.00')},
            {"numero_factura": "FACT-010", "descuento": Decimal('12.50")}
        ]
        
        ventas = []
        for i, data in enumerate(ventas_data):
            data['cliente'] = clientes[i % len(clientes)]
            venta = Venta.objects.create(**data)
            ventas.append(venta)
            print(f"✅ Venta creada: {venta}")
        
        # Crear Detalles de Venta
        detalles_data = [
            {"venta": ventas[0], "producto": productos[0], "cantidad": 1},
            {"venta": ventas[0], "producto": productos[6], "cantidad": 2},
            {"venta": ventas[1], "producto": productos[1], "cantidad": 1},
            {"venta": ventas[1], "producto": productos[3], "cantidad": 1},
            {"venta": ventas[2], "producto": productos[12], "cantidad": 1},
            {"venta": ventas[2], "producto": productos[14], "cantidad": 2},
            {"venta": ventas[3], "producto": productos[7], "cantidad": 3},
            {"venta": ventas[3], "producto": productos[8], "cantidad": 1},
            {"venta": ventas[4], "producto": productos[17], "cantidad": 1},
            {"venta": ventas[4], "producto": productos[18], "cantidad": 2},
            {"venta": ventas[5], "producto": productos[23], "cantidad": 5},
            {"venta": ventas[5], "producto": productos[24], "cantidad": 3},
            {"venta": ventas[6], "producto": productos[2], "cantidad": 1},
            {"venta": ventas[6], "producto": productos[4], "cantidad": 1},
            {"venta": ventas[7], "producto": productos[9], "cantidad": 1},
            {"venta": ventas[7], "producto": productos[10], "cantidad": 2},
            {"venta": ventas[8], "producto": productos[15], "cantidad": 1},
            {"venta": ventas[8], "producto": productos[16], "cantidad": 1},
            {"venta": ventas[9], "producto": productos[19], "cantidad": 1},
            {"venta": ventas[9], "producto": productos[20], "cantidad": 2},
            {"venta": ventas[9], "producto": productos[21], "cantidad": 1},
            {"venta": ventas[0], "producto": productos[5], "cantidad": 1},
            {"venta": ventas[1], "producto": productos[11], "cantidad": 1},
            {"venta": ventas[2], "producto": productos[22], "cantidad": 1},
            {"venta": ventas[3], "producto": productos[25], "cantidad": 2}
        ]
        
        for data in detalles_data:
            data['precio_momento'] = data['producto'].precio
            detalle = DetalleVenta.objects.create(**data)
            print(f"✅ Detalle creado: {detalle}")
        
        print("\n🎉 ¡Datos creados exitosamente!")
        print(f"📊 Resumen:")
        print(f"   - Direcciones: {Direccion.objects.count()}")
        print(f"   - Categorías: {Categoria.objects.count()}")
        print(f"   - Proveedores: {Proveedor.objects.count()}")
        print(f"   - Clientes: {Cliente.objects.count()}")
        print(f"   - Teléfonos: {TelefonoCliente.objects.count()}")
        print(f"   - Productos: {Producto.objects.count()}")
        print(f"   - Ventas: {Venta.objects.count()}")
        print(f"   - Detalles de Venta: {DetalleVenta.objects.count()}")
```

### Datos Ficticios Generados

**Direcciones (10 registros):**
- Av. Libertador 1234, Las Condes, Santiago
- Calle Principal 567, Providencia, Santiago
- Av. Grecia 890, Ñuñoa, Santiago
- Calle Comercio 123, Valparaíso, Valparaíso
- Av. Brasil 456, Valparaíso, Valparaíso
- Calle Arturo Prat 789, Concepción, Concepción
- Av. Colón 321, Concepción, Concepción
- Calle Baquedano 654, La Serena, La Serena
- Av. Francisco de Aguirre 987, La Serena, La Serena
- Calle Zenteno 147, Antofagasta, Antofagasta

**Categorías (5 registros):**
- Electrónicos: Dispositivos electrónicos y tecnología
- Ropa: Vestimenta y accesorios
- Hogar: Artículos para el hogar
- Deportes: Equipamiento deportivo
- Libros: Literatura y material educativo

**Proveedores (8 registros):**
- PROV001 - TechnoSupply Ltda.
- PROV002 - Distribuidora Central
- PROV003 - Importadora Global
- PROV004 - Textiles del Sur
- PROV005 - Hogar y Más
- PROV006 - Deportes Extremos
- PROV007 - Editorial Conocimiento
- PROV008 - Mega Distribuidora

**Clientes (15 registros):**
- CLI001 - Juan Pérez González
- CLI002 - María García López
- CLI003 - Carlos Rodríguez Silva
- CLI004 - Ana Martínez Torres
- CLI005 - Luis Fernández Ruiz
- CLI006 - Carmen Sánchez Morales
- CLI007 - Roberto Díaz Herrera
- CLI008 - Patricia Jiménez Castro
- CLI009 - Miguel Vargas Peña
- CLI010 - Isabel Romero Vega
- CLI011 - Francisco Muñoz Soto
- CLI012 - Claudia Herrera Ramos
- CLI013 - Andrés Castillo Flores
- CLI014 - Mónica Guerrero Mendoza
- CLI015 - Ricardo Moreno Aguilar

**Productos (30 registros):**
- Laptop Dell Inspiron - $899.99 (Electrónicos)
- Smartphone Samsung Galaxy - $699.99 (Electrónicos)
- Tablet iPad Air - $599.99 (Electrónicos)
- Auriculares Bluetooth - $149.99 (Electrónicos)
- Monitor 24 pulgadas - $299.99 (Electrónicos)
- Teclado Mecánico - $89.99 (Electrónicos)
- Mouse Inalámbrico - $39.99 (Electrónicos)
- Camiseta Polo - $29.99 (Ropa)
- Jeans Clásicos - $79.99 (Ropa)
- Chaqueta de Cuero - $199.99 (Ropa)
- Zapatos Deportivos - $119.99 (Ropa)
- Vestido Elegante - $89.99 (Ropa)
- Sofá 3 Plazas - $799.99 (Hogar)
- Mesa de Comedor - $499.99 (Hogar)
- Lámpara de Pie - $129.99 (Hogar)
- Aspiradora Robot - $349.99 (Hogar)
- Microondas - $199.99 (Hogar)
- Bicicleta Montaña - $599.99 (Deportes)
- Pelota de Fútbol - $29.99 (Deportes)
- Raqueta de Tenis - $149.99 (Deportes)
- Pesas Ajustables - $199.99 (Deportes)
- Cinta de Correr - $899.99 (Deportes)
- Casco de Ciclismo - $79.99 (Deportes)
- El Quijote - $19.99 (Libros)
- Cien Años de Soledad - $24.99 (Libros)
- Manual de Python - $49.99 (Libros)
- Historia de Chile - $34.99 (Libros)
- Diccionario Español - $29.99 (Libros)
- Atlas Mundial - $39.99 (Libros)
- Enciclopedia Infantil - $59.99 (Libros)

**Ventas (10 registros):**
- FACT-001 - Juan Pérez González (5% descuento)
- FACT-002 - María García López (0% descuento)
- FACT-003 - Carlos Rodríguez Silva (10% descuento)
- FACT-004 - Ana Martínez Torres (2.5% descuento)
- FACT-005 - Luis Fernández Ruiz (0% descuento)
- FACT-006 - Carmen Sánchez Morales (7.5% descuento)
- FACT-007 - Roberto Díaz Herrera (15% descuento)
- FACT-008 - Patricia Jiménez Castro (0% descuento)
- FACT-009 - Miguel Vargas Peña (5% descuento)
- FACT-010 - Isabel Romero Vega (12.5% descuento)

**Detalles de Venta (25 registros):**
- FACT-001: Laptop Dell Inspiron (x1), Mouse Inalámbrico (x2), Teclado Mecánico (x1)
- FACT-002: Smartphone Samsung Galaxy (x1), Auriculares Bluetooth (x1), Vestido Elegante (x1)
- FACT-003: Sofá 3 Plazas (x1), Lámpara de Pie (x2), Casco de Ciclismo (x1)
- FACT-004: Camiseta Polo (x3), Jeans Clásicos (x1), Manual de Python (x2)
- FACT-005: Bicicleta Montaña (x1), Pelota de Fútbol (x2)
- FACT-006: El Quijote (x5), Cien Años de Soledad (x3)
- FACT-007: Tablet iPad Air (x1), Monitor 24 pulgadas (x1)
- FACT-008: Chaqueta de Cuero (x1), Zapatos Deportivos (x2)
- FACT-009: Aspiradora Robot (x1), Microondas (x1)
- FACT-010: Raqueta de Tenis (x1), Pesas Ajustables (x2), Cinta de Correr (x1)

### Resumen de Datos
- **Total de registros:** 95
- **Tablas creadas:** 8
- **Relaciones implementadas:** 7
- **Validaciones activas:** Códigos únicos, precios positivos, stock no negativo
- **Cálculos automáticos:** Montos de detalles y ventas