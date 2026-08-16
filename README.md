# Calculate Order Total - Test Suite

Proyecto de testing en Python con pytest para validar una función que calcula el total de pedidos con descuentos opcionales.

## Descripción

Este proyecto contiene una suite completa de tests para la función `calculate_order_total` que:
- Calcula el total de un pedido basado en una lista de items
- Aplica descuentos del 10% si es solicitado
- Valida que los datos sean correctos
- Redondea los resultados a 2 decimales

## Funcionalidad

### Función Principal: `calculate_order_total(items, apply_discount=False)`

**Parámetros:**
- `items` (List): Lista de diccionarios con claves 'price' y 'quantity'
- `apply_discount` (bool): Si aplica descuento del 10%

**Retorna:**
- float: Total del pedido redondeado a 2 decimales

**Validaciones:**
- Lista no puede estar vacía
- Cada item debe tener 'price' y 'quantity'
- Price y quantity deben ser mayores a 0

## Tests Incluidos

### 1. Test de Lista Vacía
- ✅ Valida error con lista vacía
- ✅ Valida error con None

### 2. Test sin Descuento
- ✅ Item único: $50 × 1 = $50
- ✅ Múltiples items: ($50 × 1) + ($25 × 2) = $100

### 3. Test con Descuento
- ✅ Item único con descuento: $50 - 10% = $45
- ✅ Múltiples items con descuento: $100 - 10% = $90

### 4. Test de Validación
- ✅ Falta clave 'price'
- ✅ Falta clave 'quantity'
- ✅ Price = 0
- ✅ Quantity = 0
- ✅ Price negativo
- ✅ Quantity negativo

### 5. Test de Redondeo
- ✅ Redondeo sin descuento
- ✅ Redondeo con descuento
- ✅ Redondeo múltiples items

## Estructura del Proyecto

```
certif-python/
├── main.py                                    # Función principal
├── tests/
│   ├── conftest.py                           # Fixtures compartidos
│   ├── test_calculate_total_empty_list.py    # Tests de lista vacía
│   ├── test_calculate_total_no_discount.py   # Tests sin descuento
│   ├── test_calculate_total_with_discount.py # Tests con descuento
│   ├── test_calculate_total_validation_error.py # Tests de validación
│   └── test_rounding_behavior.py             # Tests de redondeo
└── README.md                                  # Este archivo
```

## Instalación y Uso

### Requisitos
- Python 3.7+
- pytest

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/certif-python.git
cd certif-python

# Crear un entorno virtual (opcional)
python -m venv .venv
source .venv/Scripts/activate  # Windows

# Instalar pytest
pip install pytest pytest-cov
```

### Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con verbose
pytest -v

# Ejecutar con cobertura
pytest --cov=main --cov-report=term-missing
```

## Ejemplo de Uso

```python
from main import calculate_order_total

# Sin descuento
items = [
    {'price': 50.0, 'quantity': 1},
    {'price': 25.0, 'quantity': 2}
]
total = calculate_order_total(items, apply_discount=False)
print(total)  # 100.0

# Con descuento del 10%
total_with_discount = calculate_order_total(items, apply_discount=True)
print(total_with_discount)  # 90.0
```

## Estado de Tests

✅ **Todos los tests pasan correctamente**

- Total de tests: 14
- Cobertura: 100%

## Autor

Proyecto educativo de testing en Python
