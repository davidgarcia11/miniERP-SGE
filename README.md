# MiniERP - Sistema de Gestión Empresarial

## Fase 1: Análisis y Modelado de Datos

### 1.1 Justificación del Modelo

#### Entidades Maestros (Datos de Referencia):
- **Cliente**: Información de clientes que realizan compras. Contiene datos como razón social, CIF/NIF, datos de contacto y dirección fiscal.
- **Producto**: Catálogo de productos disponibles para la venta. Incluye SKU único, nombre, descripción, precios (coste y venta), IVA y control de stock.
- **Estado**: Estados del ciclo de vida del pedido (ej: Pendiente, Confirmado, Facturado, Cobrado). Permite gestionar el flujo de trabajo de los pedidos.

#### Entidades Transaccionales (Operaciones de Negocio):
- **Pedido**: Cabecera del documento de venta. Representa una transacción comercial completa con un cliente en un momento determinado.
- **LineaPedido**: Detalle de cada línea del pedido. Contiene información sobre qué productos se han pedido, en qué cantidad y a qué precio.

#### Relaciones y Cardinalidades:

1. **Cliente → Pedido**: Un Cliente puede tener N Pedidos (relación 1:N)
   - Un cliente puede realizar múltiples pedidos a lo largo del tiempo
   - Un pedido pertenece a un único cliente

2. **Pedido → LineaPedido**: Un Pedido tiene N LineasPedido (relación 1:N)
   - Un pedido puede contener múltiples líneas (productos diferentes)
   - Cada línea pertenece a un único pedido
   - Si se elimina un pedido, se eliminan todas sus líneas (CASCADE)

3. **Producto → LineaPedido**: Un Producto está en N LineasPedido (relación 1:N)
   - Un producto puede aparecer en múltiples líneas de diferentes pedidos
   - Una línea referencia un único producto
   - No se puede eliminar un producto si está en algún pedido (PROTECT)

4. **Estado → Pedido**: Un Pedido tiene 1 Estado (relación N:1)
   - Un pedido tiene un único estado en cada momento
   - Los estados posibles son: BORRADOR, CONFIRMADO, FACTURADO, COBRADO

### 1.2 Diagrama Entidad-Relación

```
┌─────────────────┐
│    CLIENTE      │
├─────────────────┤
│ PK id           │
│    razon_social │
│    cif (UNIQUE) │
│    nombre_contacto│
│    email        │
│    telefono     │
│    direccion    │
└────────┬────────┘
         │
         │ 1
         │
         │ N
┌────────▼────────┐
│     PEDIDO      │
├─────────────────┤
│ PK id           │
│ FK cliente_id   │
│    estado       │
│    (BORRADOR,   │
│     CONFIRMADO, │
│     FACTURADO,  │
│     COBRADO)    │
│    fecha_creacion│
│    direccion_envio│
│    observaciones │
└────────┬─────────┘
         │
         │ 1
         │
         │ N
┌────────▼──────────┐
│   LINEA_PEDIDO    │
├───────────────────┤
│ PK id             │
│ FK pedido_id      │
│ FK producto_id    │
│    cantidad (>0)  │
│    precio_unitario│
│    descuento      │
└────────┬──────────┘
         │
         │ N
         │
         │ 1
┌────────▼────────┐
│   PRODUCTO      │
├─────────────────┤
│ PK id           │
│    sku (UNIQUE) │
│    nombre       │
│    descripcion  │
│    coste        │
│    precio       │
│    iva          │
│    stock        │
│    activo       │
└─────────────────┘
```

**Leyenda:**
- PK = Primary Key (Clave Primaria)
- FK = Foreign Key (Clave Foránea)
- UNIQUE = Restricción de unicidad
- (>0) = Constraint de validación
- 1:N = Relación uno a muchos
- N:1 = Relación muchos a uno

## Estructura del Proyecto

```
miniERP-SGE/
├── manage.py
├── erp/                    # Proyecto Django principal
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                   # App de datos maestros
│   ├── models.py          # Cliente, Producto
│   ├── admin.py
│   └── migrations/
└── ventas/                 # App de operaciones transaccionales
    ├── models.py          # Pedido, LineaPedido
    ├── admin.py
    └── migrations/
```

## Tecnologías Utilizadas

- Django 4.2.27
- Python 3.x
- SQLite (base de datos por defecto)

## Instalación y Uso

### Requisitos Previos
- Python 3.9 o superior
- pip (gestor de paquetes de Python)

### Configuración del Entorno Virtual

1. **Crear entorno virtual** (si no existe):
   ```
   python3 -m venv venv
   ```

2. **Activar entorno virtual**:
   - En macOS/Linux: `source venv/bin/activate`
   - En Windows: `venv\Scripts\activate`

3. **Instalar dependencias**:
   ```
   pip install -r requirements.txt
   ```

### Uso del Proyecto

1. **Activar el entorno virtual** (si no está activo):
   ```
   source venv/bin/activate  # macOS/Linux
   ```

2. **Aplicar migraciones**:
   ```
   python manage.py migrate
   ```

3. **Crear superusuario** (opcional):
   ```
   python manage.py createsuperuser
   ```

4. **Ejecutar servidor de desarrollo**:
   ```
   python manage.py runserver
   ```

5. **Acceder al admin**: `http://localhost:8000/admin`

### Notas Importantes

- **Siempre activa el entorno virtual** antes de trabajar en el proyecto
- El entorno virtual (`venv/`) está en `.gitignore` y no se sube al repositorio
- Las dependencias están documentadas en `requirements.txt`
- Para desactivar el entorno virtual, ejecuta: `deactivate`

