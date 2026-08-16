# Exercises: Test-Driven Development in Python

Una progresión de ejercicios prácticos sobre testing en Python, desde pruebas
unitarias hasta integración con bases de datos.

---

## 🎯 Ejercicio 1: Unit Testing (Rama: main)

**Objetivo**: Dominar pruebas unitarias con pytest para una función de cálculo
de totales de pedidos.

### Función: `calculate_order_total(items, apply_discount=False)`

Calcula el total de un pedido aplicando validaciones y descuentos opcionales.

**Parámetros:**

- `items` (List[Dict]): Lista de items con 'price' y 'quantity'
- `apply_discount` (bool): Aplica descuento del 10%

**Retorna:** float (redondeado a 2 decimales)

### Test Suites

#### 1️⃣ Validación de Lista Vacía

```python
class TestEmptyList:
    def test_empty_list_raise_error()
    def test_none_raise_error()
```

✅ Verifica que la función rechaza listas vacías y None

#### 2️⃣ Cálculo sin Descuento

```python
class TestCalculateTotalNoDiscount:
    def test_single_item_no_discount()
    def test_multiple_items_no_discount()
```

✅ Valida cálculos correctos sin aplicar descuento

#### 3️⃣ Cálculo con Descuento

```python
class TestCalculateTotalWithDiscount:
    def test_single_item_with_discount()
    def test_multiple_items_with_discount()
```

✅ Verifica aplicación correcta del descuento del 10%

#### 4️⃣ Validación de Items

```python
class TestRaiseItemValidationErrors:
    @pytest.mark.parametrize(...)
    def test_raise_item_validation_error()
```

✅ Cubre 6 casos de validación:

- Falta clave 'price'
- Falta clave 'quantity'
- Price = 0
- Quantity = 0
- Price negativo
- Quantity negativo

#### 5️⃣ Comportamiento de Redondeo

```python
class TestRoundingBehavior:
    def test_rounding_to_two_decimals_without_discount()
    def test_rounding_to_two_decimals_with_discount()
    def test_rounding_multiple_items_with_discount()
```

✅ Valida redondeo preciso a 2 decimales

### Fixtures Compartidos

```python
@pytest.fixture
def single_item():
    return [{'price': 50.0, 'quantity': 1}]

@pytest.fixture
def multiple_items():
    return [
        {'price': 50.0, 'quantity': 1},
        {'price': 25.0, 'quantity': 2}
    ]
```

### Ejecutar Tests

```bash
pytest tests/ -v
pytest tests/ --cov=main --cov-report=term-missing
```

**Resultado:** ✅ **14 tests** - 100% cobertura

---

## 🗄️ Ejercicio 2: Database Integration (Rama: feature/database)

**Objetivo**: Integrar pruebas unitarias con persistencia en SQLite y
operaciones CRUD.

### Módulos

#### `database.py`

Clase `OrderDatabase` que gestiona:

**Orders Table:**

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    total REAL,
    discount_applied INTEGER,
    created_at TIMESTAMP
)
```

**Order Items Table:**

```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER FK,
    price REAL,
    quantity INTEGER
)
```

**Users Table:**

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    email TEXT
)
```

**Métodos:**

- `save_order(items, total, discount_applied) → order_id`
- `get_order(order_id) → Dict`
- `get_all_orders() → List[Dict]`
- `save_user(username, email) → user_id`
- `get_user_by_username(username) → Dict`
- `clear_database()`

#### `order_service.py`

```python
def calculate_and_save_order(items, apply_discount=False, db_path="orders.db"):
    total = calculate_order_total(items, apply_discount)
    db = OrderDatabase(db_path)
    order_id = db.save_order(items, total, apply_discount)
    return total, order_id
```

### Test Suites

#### 1️⃣ Integración de Órdenes

```python
class TestOrderDatabase:
    def test_save_and_retrieve_order_without_discount()
    def test_save_and_retrieve_order_with_discount()
    def test_save_multiple_items_order()
    def test_get_all_orders()
    def test_order_id_increments()
```

✅ Valida operaciones CRUD de órdenes

#### 2️⃣ Gestión de Usuarios

```python
class TestSaveAndGetUser:
    def test_save_and_get_user()
    def test_save_user_via_connection()
```

✅ Cubre crear y recuperar usuarios

### Fixture para Conexión a BD

```python
@pytest.fixture
def db_connection(tmp_path):
    db_path = str(tmp_path / "test_db.sqlite")
    OrderDatabase(db_path)
    conn = sqlite3.connect(db_path)
    yield conn
    conn.close()
```

### Ejecutar Tests

```bash
git checkout feature/database
pytest tests/test_database_integration.py -v
pytest tests/test_database_users.py -v
```

**Resultado:** ✅ **6 tests de integración** + **2 tests de usuarios**

---

## 🏗️ Estructura del Proyecto

```
certif-python/
├── main.py
├── database.py
├── order_service.py
├── tests/
│   ├── conftest.py
│   ├── test_calculate_total_empty_list.py
│   ├── test_calculate_total_no_discount.py
│   ├── test_calculate_total_with_discount.py
│   ├── test_calculate_total_validation_error.py
│   ├── test_rounding_behavior.py
│   ├── test_database_integration.py
│   └── test_database_users.py
├── README.md
└── DATABASE_BRANCH.md
```

---

## 📚 Ramas

### `main`

- Ejercicio 1: Unit Testing
- 14 tests unitarios
- 100% cobertura

### `feature/database`

- Ejercicio 2: Database Integration
- 8 tests de integración con BD
- SQLite + CRUD operations
- User management

### `feature/api-rest` (próximo)

- Ejercicio 3: REST API
- FastAPI / Flask
- Integration con base de datos
- Tests de endpoints

---

## 🚀 Quick Start

### Clonar y configurar

```bash
git clone <repo>
cd certif-python
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install pytest pytest-cov
```

### Ejercicio 1: Unit Tests

```bash
git checkout main
pytest tests/ -v
```

### Ejercicio 2: Database Integration

```bash
git checkout feature/database
pytest tests/ -v
```

---

## 📊 Resultados

| Ejercicio            | Tests | Cobertura | Estado |
| -------------------- | ----- | --------- | ------ |
| Unit Testing         | 14    | 100%      | ✅     |
| Database Integration | 8     | 100%      | ✅     |
| REST API             | TBD   | TBD       | 🔄     |

---

## 🎓 Conceptos Cubiertos

✅ Pytest fixtures y parametrización\
✅ Validación y manejo de errores\
✅ Testing de bordes (edge cases)\
✅ SQLite con Python\
✅ CRUD operations\
✅ Integración de tests\
✅ Cobertura de código\
✅ Cleanup de recursos temporales

---

**Autor**: Proyecto educativo de TDD en Python
