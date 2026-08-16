# Database Integration Branch

Esta rama (`feature/database`) agrega integración con SQLite para persistir los pedidos.

## Nuevos Archivos

### `database.py`
Clase `OrderDatabase` que maneja:
- Creación de tablas (orders y order_items)
- Guardado de pedidos
- Recuperación de pedidos
- Limpieza de base de datos

### `order_service.py`
Función `calculate_and_save_order` que:
- Calcula el total usando `calculate_order_total`
- Guarda el pedido en la base de datos
- Retorna el total y el ID del pedido

### `tests/test_database_integration.py`
Tests para:
- Guardar y recuperar pedidos sin descuento
- Guardar y recuperar pedidos con descuento
- Guardar pedidos con múltiples items
- Recuperar todos los pedidos
- Verificar incremento de IDs

## Uso

```python
from order_service import calculate_and_save_order

items = [
    {'price': 50.0, 'quantity': 1},
    {'price': 25.0, 'quantity': 2}
]

total, order_id = calculate_and_save_order(items, apply_discount=True)
print(f"Total: ${total}, Order ID: {order_id}")
```

## Estructura de Base de Datos

### Tabla `orders`
```sql
id INTEGER PRIMARY KEY
total REAL
discount_applied INTEGER (0 o 1)
created_at TIMESTAMP
```

### Tabla `order_items`
```sql
id INTEGER PRIMARY KEY
order_id INTEGER (FK)
price REAL
quantity INTEGER
```

## Para Volver a main

```bash
git checkout main
```

## Para Fusionar esta rama a main

```bash
git checkout main
git merge feature/database
git push origin main
```

## Para Eliminar esta rama

```bash
git branch -d feature/database
```
