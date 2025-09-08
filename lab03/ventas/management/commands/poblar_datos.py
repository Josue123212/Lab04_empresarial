from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal
import random
from datetime import datetime, timedelta

from ventas.models import (
    Direccion,
    TelefonoCliente,
    Categoria,
    Proveedor,
    Cliente,
    Producto,
    Venta,
    DetalleVenta
)

class Command(BaseCommand):
    help = 'Poblar la base de datos con datos ficticios para el sistema de ventas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Limpiar datos existentes antes de poblar',
        )

    def handle(self, *args, **options):
        if options['limpiar']:
            self.stdout.write(self.style.WARNING('Limpiando datos existentes...'))
            self.limpiar_datos()

        self.stdout.write(self.style.SUCCESS('Iniciando población de datos...'))
        
        with transaction.atomic():
            # Crear datos en orden de dependencias
            direcciones = self.crear_direcciones()
            categorias = self.crear_categorias()
            proveedores = self.crear_proveedores(direcciones)
            clientes = self.crear_clientes(direcciones)
            self.crear_telefonos_clientes(clientes)
            productos = self.crear_productos(categorias, proveedores)
            ventas = self.crear_ventas(clientes)
            self.crear_detalles_ventas(ventas, productos)

        self.stdout.write(
            self.style.SUCCESS('¡Datos poblados exitosamente!')
        )

    def limpiar_datos(self):
        """Eliminar todos los datos existentes"""
        DetalleVenta.objects.all().delete()
        Venta.objects.all().delete()
        Producto.objects.all().delete()
        TelefonoCliente.objects.all().delete()
        Cliente.objects.all().delete()
        Proveedor.objects.all().delete()
        Categoria.objects.all().delete()
        Direccion.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Datos limpiados'))

    def crear_direcciones(self):
        """Crear direcciones de ejemplo"""
        direcciones_data = [
            {'calle': 'Av. Libertador', 'numero': '1234', 'comuna': 'Las Condes', 'ciudad': 'Santiago'},
            {'calle': 'Calle Moneda', 'numero': '567', 'comuna': 'Santiago Centro', 'ciudad': 'Santiago'},
            {'calle': 'Av. Providencia', 'numero': '890', 'comuna': 'Providencia', 'ciudad': 'Santiago'},
            {'calle': 'Calle Huérfanos', 'numero': '321', 'comuna': 'Santiago Centro', 'ciudad': 'Santiago'},
            {'calle': 'Av. Apoquindo', 'numero': '654', 'comuna': 'Las Condes', 'ciudad': 'Santiago'},
            {'calle': 'Calle Bandera', 'numero': '987', 'comuna': 'Santiago Centro', 'ciudad': 'Santiago'},
            {'calle': 'Av. Vitacura', 'numero': '147', 'comuna': 'Vitacura', 'ciudad': 'Santiago'},
            {'calle': 'Calle Estado', 'numero': '258', 'comuna': 'Santiago Centro', 'ciudad': 'Santiago'},
        ]
        
        direcciones = []
        for data in direcciones_data:
            direccion = Direccion.objects.create(**data)
            direcciones.append(direccion)
            
        self.stdout.write(f'Creadas {len(direcciones)} direcciones')
        return direcciones

    def crear_categorias(self):
        """Crear categorías de productos"""
        categorias_data = [
            {'nombre': 'Electrónicos', 'descripcion': 'Dispositivos electrónicos y tecnología'},
            {'nombre': 'Ropa', 'descripcion': 'Vestimenta y accesorios'},
            {'nombre': 'Hogar', 'descripcion': 'Artículos para el hogar y decoración'},
            {'nombre': 'Deportes', 'descripcion': 'Equipamiento deportivo y fitness'},
            {'nombre': 'Libros', 'descripcion': 'Literatura y material educativo'},
        ]
        
        categorias = []
        for data in categorias_data:
            categoria = Categoria.objects.create(**data)
            categorias.append(categoria)
            
        self.stdout.write(f'Creadas {len(categorias)} categorías')
        return categorias

    def crear_proveedores(self, direcciones):
        """Crear proveedores"""
        proveedores_data = [
            {'codigo': 'PROV001', 'nombre': 'TechnoSupply SpA', 'telefono': '+56912345678', 'web': 'https://technosupply.cl'},
            {'codigo': 'PROV002', 'nombre': 'Distribuidora Central', 'telefono': '+56987654321', 'web': 'https://distcentral.cl'},
            {'codigo': 'PROV003', 'nombre': 'Importadora Global', 'telefono': '+56911223344', 'web': 'https://impglobal.cl'},
            {'codigo': 'PROV004', 'nombre': 'Comercial del Sur', 'telefono': '+56955667788', 'web': 'https://comsur.cl'},
            {'codigo': 'PROV005', 'nombre': 'Mayorista Express', 'telefono': '+56933445566', 'web': 'https://mayexpress.cl'},
        ]
        
        proveedores = []
        for i, data in enumerate(proveedores_data):
            direccion = random.choice(direcciones)
            proveedor = Proveedor.objects.create(
                direccion=direccion,
                **data
            )
            proveedores.append(proveedor)
            
        self.stdout.write(f'Creados {len(proveedores)} proveedores')
        return proveedores

    def crear_clientes(self, direcciones):
        """Crear clientes"""
        clientes_data = [
            {'codigo': 'CLI001', 'nombre': 'Juan Pérez González'},
            {'codigo': 'CLI002', 'nombre': 'María García López'},
            {'codigo': 'CLI003', 'nombre': 'Carlos Rodríguez Silva'},
            {'codigo': 'CLI004', 'nombre': 'Ana Martínez Torres'},
            {'codigo': 'CLI005', 'nombre': 'Luis Fernández Ruiz'},
            {'codigo': 'CLI006', 'nombre': 'Carmen Sánchez Morales'},
            {'codigo': 'CLI007', 'nombre': 'Roberto Díaz Herrera'},
            {'codigo': 'CLI008', 'nombre': 'Patricia Jiménez Castro'},
            {'codigo': 'CLI009', 'nombre': 'Miguel Vargas Mendoza'},
            {'codigo': 'CLI010', 'nombre': 'Isabel Romero Vega'},
        ]
        
        clientes = []
        for data in clientes_data:
            direccion = random.choice(direcciones)
            cliente = Cliente.objects.create(
                direccion=direccion,
                **data
            )
            clientes.append(cliente)
            
        self.stdout.write(f'Creados {len(clientes)} clientes')
        return clientes

    def crear_telefonos_clientes(self, clientes):
        """Crear teléfonos para clientes"""
        telefonos_base = [
            '+56912345678', '+56987654321', '+56911223344',
            '+56955667788', '+56933445566', '+56977889900',
            '+56944556677', '+56966778899', '+56922334455',
            '+56988776655', '+56999887766', '+56911998877'
        ]
        
        telefonos_creados = 0
        for cliente in clientes:
            # Cada cliente tiene entre 1 y 3 teléfonos
            num_telefonos = random.randint(1, 3)
            telefonos_cliente = random.sample(telefonos_base, num_telefonos)
            
            for telefono in telefonos_cliente:
                TelefonoCliente.objects.create(
                    cliente=cliente,
                    numero=telefono
                )
                telefonos_creados += 1
                
        self.stdout.write(f'Creados {telefonos_creados} teléfonos')

    def crear_productos(self, categorias, proveedores):
        """Crear productos"""
        productos_data = [
            {'nombre': 'Smartphone Galaxy S23', 'precio': Decimal('899.99'), 'stock': 25},
            {'nombre': 'Laptop Dell Inspiron', 'precio': Decimal('1299.99'), 'stock': 15},
            {'nombre': 'Auriculares Bluetooth', 'precio': Decimal('199.99'), 'stock': 50},
            {'nombre': 'Camiseta Deportiva', 'precio': Decimal('29.99'), 'stock': 100},
            {'nombre': 'Pantalón Jeans', 'precio': Decimal('79.99'), 'stock': 75},
            {'nombre': 'Zapatillas Running', 'precio': Decimal('149.99'), 'stock': 40},
            {'nombre': 'Mesa de Centro', 'precio': Decimal('299.99'), 'stock': 20},
            {'nombre': 'Lámpara LED', 'precio': Decimal('89.99'), 'stock': 60},
            {'nombre': 'Silla Ergonómica', 'precio': Decimal('399.99'), 'stock': 30},
            {'nombre': 'Libro Python Programming', 'precio': Decimal('49.99'), 'stock': 80},
            {'nombre': 'Tablet iPad Air', 'precio': Decimal('699.99'), 'stock': 35},
            {'nombre': 'Reloj Inteligente', 'precio': Decimal('299.99'), 'stock': 45},
            {'nombre': 'Mochila Deportiva', 'precio': Decimal('59.99'), 'stock': 90},
            {'nombre': 'Cafetera Automática', 'precio': Decimal('199.99'), 'stock': 25},
            {'nombre': 'Monitor 24 pulgadas', 'precio': Decimal('349.99'), 'stock': 20},
        ]
        
        productos = []
        for data in productos_data:
            categoria = random.choice(categorias)
            producto = Producto.objects.create(
                categoria=categoria,
                **data
            )
            
            # Asignar proveedores aleatorios (1-3 proveedores por producto)
            num_proveedores = random.randint(1, 3)
            proveedores_producto = random.sample(proveedores, num_proveedores)
            producto.proveedores.set(proveedores_producto)
            
            productos.append(producto)
            
        self.stdout.write(f'Creados {len(productos)} productos')
        return productos

    def crear_ventas(self, clientes):
        """Crear ventas"""
        ventas = []
        
        for i in range(10):
            # Generar fecha aleatoria en los últimos 30 días
            fecha_base = datetime.now() - timedelta(days=30)
            fecha_venta = fecha_base + timedelta(days=random.randint(0, 30))
            
            venta = Venta.objects.create(
                numero_factura=f'FAC{str(i+1).zfill(6)}',
                cliente=random.choice(clientes),
                descuento=Decimal(str(random.uniform(0, 15))),  # Descuento 0-15%
                monto=Decimal('0.00')  # Se calculará después
            )
            # Actualizar la fecha manualmente
            venta.fecha = fecha_venta
            venta.save()
            
            ventas.append(venta)
            
        self.stdout.write(f'Creadas {len(ventas)} ventas')
        return ventas

    def crear_detalles_ventas(self, ventas, productos):
        """Crear detalles de ventas"""
        detalles_creados = 0
        
        for venta in ventas:
            # Cada venta tiene entre 1 y 5 productos
            num_productos = random.randint(1, 5)
            productos_venta = random.sample(productos, num_productos)
            
            monto_total_venta = Decimal('0.00')
            
            for producto in productos_venta:
                cantidad = random.randint(1, 5)
                precio_momento = producto.precio
                monto_total = precio_momento * cantidad
                
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    precio_momento=precio_momento,
                    cantidad=cantidad,
                    monto_total=monto_total
                )
                
                monto_total_venta += monto_total
                detalles_creados += 1
            
            # Actualizar monto de la venta
            descuento_monto = monto_total_venta * (venta.descuento / 100)
            venta.monto = monto_total_venta - descuento_monto
            venta.save()
            
        self.stdout.write(f'Creados {detalles_creados} detalles de venta')