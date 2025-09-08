# 📋 PLAN DE DESARROLLO - SISTEMA DE VENTAS

## 🎯 ANÁLISIS DE LA APP ENCUESTA ACTUAL

### Estructura Actual:
- **Modelos**: Pregunta y Opcion con relación ForeignKey
- **Admin**: Configuración avanzada con inlines y filtros
- **Views**: Funciones básicas para mostrar y procesar datos
- **URLs**: Rutas organizadas con namespace
- **Templates**: Estructura HTML básica

### Patrones Identificados:
✅ Relaciones entre modelos (ForeignKey)
✅ Métodos personalizados en modelos (__str__, was_published_recently)
✅ Configuración del admin con inlines
✅ Organización de URLs con app_name
✅ Context processors en views

---

## 🏗️ ESQUEMA DE CLASES - SISTEMA DE VENTAS

### 📊 DIAGRAMA DE ENTIDADES

```
Dirección
├── calle: CharField
├── numero: CharField
├── comuna: CharField
└── ciudad: CharField

Proveedor
├── codigo: CharField (unique)
├── nombre: CharField
├── direccion: ForeignKey(Dirección)
├── telefono: CharField
└── pagina_web: URLField

Cliente
├── codigo: CharField (unique)
├── nombre: CharField
├── direccion: ForeignKey(Dirección)
└── telefonos: ManyToMany(TelefonoCliente)

TelefonoCliente
├── cliente: ForeignKey(Cliente)
└── numero: CharField

Categoria
├── id: AutoField
├── nombre: CharField
└── descripcion: TextField

Producto
├── id: AutoField
├── nombre: CharField
├── precio_actual: DecimalField
├── stock: IntegerField
├── categoria: ForeignKey(Categoria)
└── proveedores: ManyToMany(Proveedor)

Venta
├── numero_factura: CharField (unique)
├── fecha: DateTimeField
├── cliente: ForeignKey(Cliente)
├── descuento: DecimalField
├── monto_final: DecimalField
└── productos: ManyToMany(Producto, through='DetalleVenta')

DetalleVenta
├── venta: ForeignKey(Venta)
├── producto: ForeignKey(Producto)
├── precio_momento_venta: DecimalField
├── cantidad: IntegerField
└── monto_total: DecimalField
```

---

## 🚀 FASES DE IMPLEMENTACIÓN

### FASE 1: Configuración Inicial

**Paso 1: Crear nueva app 'ventas'**
- [x] Navegar al directorio del proyecto Django
- [x] Ejecutar `python manage.py startapp ventas`
- [x] Verificar que se creó la carpeta `ventas/` con archivos base
- [x] Confirmar estructura: `models.py`, `views.py`, `admin.py`, `apps.py`

**Paso 2: Configurar INSTALLED_APPS**
- [x] Abrir `lab03/settings.py`
- [x] Agregar `'ventas',` a la lista INSTALLED_APPS
- [x] Guardar el archivo
- [x] Verificar que no hay errores de sintaxis

### FASE 2: Modelos Base (Orden de Dependencias)

**Paso 3: Modelo Direccion**
- [x] Abrir `ventas/models.py`
- [x] Importar `from django.db import models`
- [x] Crear clase `Direccion` con campos: calle, numero, comuna, ciudad
- [x] Agregar método `__str__`
- [x] Verificar sintaxis del modelo

**Paso 4: Modelo TelefonoCliente**
- [x] Crear clase `TelefonoCliente` en `models.py`
- [x] Definir ForeignKey a Cliente (se creará después)
- [x] Agregar campo `numero`
- [x] Implementar método `__str__`

**Paso 5: Modelo Categoria**
- [x] Crear clase `Categoria` en `models.py`
- [x] Definir campos: nombre, descripcion
- [x] Agregar método `__str__`
- [x] Validar longitudes de campos

**Paso 6: Modelo Proveedor**
- [x] Crear clase `Proveedor` en `models.py`
- [x] Definir campo `codigo` único
- [x] Agregar campos: nombre, telefono, web
- [x] Crear ForeignKey a Direccion
- [x] Implementar método `__str__`

**Paso 7: Modelo Cliente**
- [x] Crear clase `Cliente` en `models.py`
- [x] Definir campo `codigo` único
- [x] Agregar campo `nombre`
- [x] Crear ForeignKey a Direccion
- [x] Implementar método `__str__`

**Paso 8: Modelo Producto**
- [x] Crear clase `Producto` en `models.py`
- [x] Definir campos: nombre, precio, stock
- [x] Crear ForeignKey a Categoria
- [x] Crear ManyToManyField a Proveedor
- [x] Implementar método `__str__`

### FASE 3: Modelos de Transacciones

**Paso 9: Modelo Venta**
- [x] Crear clase `Venta` en `models.py`
- [x] Definir campo `numero_factura` único
- [x] Agregar campos: fecha (auto_now_add), descuento, monto
- [x] Crear ForeignKey a Cliente
- [x] Implementar método `__str__`

**Paso 10: Modelo DetalleVenta**
- [x] Crear clase `DetalleVenta` en `models.py`
- [x] Crear ForeignKey a Venta
- [x] Crear ForeignKey a Producto
- [x] Definir campos: precio_momento, cantidad, monto_total
- [x] Implementar método `__str__`

### FASE 4: Panel de Administración

**Paso 11: Configurar Admin Básico**
- [x] Abrir `ventas/admin.py`
- [x] Importar todos los modelos
- [x] Registrar modelos básicos con `admin.site.register()`
- [x] Verificar acceso al panel admin

**Paso 12: Personalizar Interfaces Admin**
- [x] Crear clases Admin personalizadas para cada modelo
- [x] Configurar `list_display` para mostrar campos importantes
- [x] Agregar `search_fields` para búsquedas
- [x] Implementar `list_filter` para filtros
- [x] Configurar `fieldsets` para organizar formularios

**Paso 13: Configurar Inlines**
- [x] Crear `TelefonoClienteInline` para Cliente
- [x] Crear `DetalleVentaInline` para Venta
- [x] Configurar `extra` y `max_num` según necesidades
- [x] Probar funcionalidad de edición inline

### FASE 5: Datos Ficticios

**Paso 14: Crear Script de Población**
- [x] Crear archivo `ventas/management/commands/poblar_datos.py`
- [x] Implementar comando personalizado de Django
- [x] Definir datos de ejemplo para cada modelo
- [x] Manejar dependencias entre modelos

**Paso 15: Generar Datos de Prueba**
- [x] Crear 5-10 direcciones de ejemplo
- [x] Generar 3-5 categorías de productos
- [x] Crear 5-8 proveedores
- [x] Generar 10-15 clientes
- [x] Crear 20-30 productos
- [x] Generar 5-10 ventas con detalles

**Paso 16: Verificar Relaciones**
- [x] Comprobar ForeignKey funcionando correctamente
- [x] Verificar ManyToMany entre Producto y Proveedor
- [x] Validar integridad referencial
- [x] Probar eliminación en cascada

### FASE 6: Migraciones y Validación

**Paso 17: Crear y Aplicar Migraciones**
- [x] Ejecutar `python manage.py makemigrations ventas`
- [x] Revisar archivos de migración generados
- [x] Ejecutar `python manage.py migrate`
- [x] Verificar que no hay errores en la migración

**Paso 18: Validación Final**
- [x] Probar creación de registros desde admin
- [x] Verificar que todos los modelos se muestran correctamente
- [x] Comprobar funcionalidad de búsqueda y filtros
- [x] Validar relaciones entre modelos
- [x] Ejecutar `python manage.py check` para verificar configuración

**Paso 19: Documentación y Limpieza**
- [ ] Documentar cualquier configuración especial
- [ ] Verificar que todos los archivos están guardados
- [ ] Hacer commit de los cambios si se usa control de versiones
- [ ] Crear backup de la base de datos con datos de prueba

---

## 📋 MODELOS DETALLADOS

### Modelo Direccion
```python
class Direccion(models.Model):
    calle = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    comuna = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
```

### Modelo TelefonoCliente
```python
class TelefonoCliente(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    numero = models.CharField(max_length=15)
```

### Modelo Categoria
```python
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
```

### Modelo Proveedor
```python
class Proveedor(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15)
    web = models.URLField(blank=True)
```

### Modelo Cliente
```python
class Cliente(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)
```

### Modelo Producto
```python
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedores = models.ManyToManyField(Proveedor)
```

### Modelo Venta
```python
class Venta(models.Model):
    numero_factura = models.CharField(max_length=20, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
```

### Modelo DetalleVenta
```python
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio_momento = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
```

### FASE 4: CONFIGURACIÓN ADMIN (Media Prioridad)

#### 4.1 Admin Avanzado
- Inlines para DetalleVenta en VentaAdmin
- Inlines para TelefonoCliente en ClienteAdmin
- Filtros y búsquedas personalizadas
- List_display optimizados

#### 4.2 Ejemplo Admin Venta
```python
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1
    readonly_fields = ('monto_total',)

class VentaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'fecha', 'cliente', 'monto_final')
    list_filter = ['fecha', 'cliente']
    search_fields = ['numero_factura', 'cliente__nombre']
    inlines = [DetalleVentaInline]
```

### FASE 5: DATOS FICTICIOS (Media Prioridad)

#### 5.1 Crear Management Command
```bash
python manage.py crear_datos_ficticios
```

#### 5.2 Datos de Ejemplo
- 5 Direcciones
- 3 Proveedores
- 5 Clientes con teléfonos
- 4 Categorías
- 15 Productos
- 10 Ventas con detalles

### FASE 6: MIGRACIONES Y VALIDACIÓN (Alta Prioridad)

#### 6.1 Crear Migraciones
```bash
python manage.py makemigrations ventas
python manage.py migrate
```

#### 6.2 Validar Integridad
- Verificar relaciones
- Probar constraints únicos
- Validar cálculos automáticos

---

## 📝 CHECKLIST DE IMPLEMENTACIÓN

### ✅ Modelos
- [ ] Dirección
- [ ] TelefonoCliente
- [ ] Categoria
- [ ] Proveedor
- [ ] Cliente
- [ ] Producto
- [ ] Venta
- [ ] DetalleVenta

### ✅ Admin
- [ ] Configurar todos los modelos
- [ ] Implementar inlines
- [ ] Agregar filtros y búsquedas
- [ ] Personalizar list_display

### ✅ Datos
- [ ] Crear management command
- [ ] Generar datos ficticios
- [ ] Validar relaciones

### ✅ Validación
- [ ] Ejecutar migraciones
- [ ] Probar admin interface
- [ ] Verificar integridad de datos

---

## 🎓 CONCEPTOS CLAVE APLICADOS

### Desde la App Encuesta:
1. **Relaciones ForeignKey**: Aplicadas en Cliente->Dirección, Producto->Categoria
2. **Métodos __str__**: Para mejor visualización en admin
3. **Admin Inlines**: Para DetalleVenta y TelefonoCliente
4. **Validaciones**: En save() de DetalleVenta

### Nuevos Conceptos:
1. **ManyToManyField**: Producto-Proveedor
2. **Through Model**: Venta-Producto a través de DetalleVenta
3. **DecimalField**: Para manejo de dinero
4. **Unique Constraints**: Para códigos y facturas
5. **Auto-cálculos**: En save() methods

---

## 🚀 PRÓXIMOS PASOS RECOMENDADOS

1. **Crear app ventas**
2. **Implementar modelos en orden de dependencias**
3. **Configurar admin básico**
4. **Ejecutar migraciones**
5. **Crear datos ficticios**
6. **Validar funcionalidad**

¿Quieres que empecemos con la implementación? 🎯