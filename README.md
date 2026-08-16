# Test-Driven Development: Progressive Exercises

Aprende TDD en Python con ejercicios progresivos: desde pruebas unitarias hasta
integración con base de datos.

## 📖 Ver la Documentación Completa

👉 **[Ir a EXERCISES.md](EXERCISES.md)** para ver la estructura completa de los
ejercicios.

## Ramas Principales

- **`main`**: Ejercicio 1 - Unit Testing (14 tests)
- **`feature/database`**: Ejercicio 2 - Database Integration (8 tests de BD)
- **`feature/api-rest`**: Ejercicio 3 - REST API (próximamente)

## Quick Start

```bash
# Clonar
git clone <repo>
cd certif-python

# Crear entorno virtual
python -m venv .venv
source .venv/Scripts/activate  # Windows

# Instalar dependencias
pip install pytest pytest-cov

# Ejercicio 1: Unit Testing
git checkout main
pytest tests/ -v

# Ejercicio 2: Database Integration
git checkout feature/database
pytest tests/ -v
```

---

Todos los detalles, estructura de tests, y ejemplos están en
[EXERCISES.md](EXERCISES.md) 📚
