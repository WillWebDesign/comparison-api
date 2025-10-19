# RUN

## 1. Crear entorno virtual

```bash
python -m venv venv   #python3 segun instalacion
source venv/bin/activate

# Windows
venv\Scripts\activate
```

## 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 3. Crear Archivo de variables de entorno

```bash
cp .env.example .env    #Ajustar valores si es necesario
```

## 4. Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

La API estará disponible en: <http://localhost:8000>

## 5. Ver documentación

- **Swagger UI → <http://localhost:8000/docs>**
- **ReDoc → <http://localhost:8000/redoc>**

## 6. Ejecutar test

```bash
pytest -v
```

## 7. Coverage

```bash
pytest --cov=app --cov-report=term-missing

# Reporte en HTML
pytest --cov=app --cov-report=term-missing --cov-report=html # htmlcov/index.html
```

## 8. Limpiar Data

```bash
cp app/data/products_backup.json app/data/products.json
```
