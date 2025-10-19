# Comparison API

API REST desarrollada con **FastAPI** para la gestión de productos y comparación de datos.
Incluye persistencia en archivo JSON, validaciones con Pydantic y cobertura completa de pruebas unitarias.

---

## Tecnologías utilizadas

- **Python 3.9+**
- **FastAPI**
- **Uvicorn**
- **Pytest**
- **HTTPX (TestClient)**
- **Pydantic**
- **JSON como almacenamiento local**

---

## Estructura del proyecto

```bash
comparison-api/
├── app/
│   ├── main.py                      # Punto de entrada de la aplicación
│   ├── api/
│   │   └── routes/
│   │       └── products_router.py   # Endpoints para productos
│   ├── core/
│   │   └── logger.py                # Configuración de logging
│   ├── models/
│   │   ├── product.py               # Modelo de datos para product con Pydantic
│   │   └── error_response.py        # Modelo de error estándar con Pydantic
│   ├── services/
│   │   └── products_service.py      # Lógica de negocio y manejo del archivo JSON
│   ├── utils/
│   │   └── config.py                # Configuración de variables globales (.env)
│   └── data/
│       └── products.json            # Archivo de persistencia
│
├── tests/
│   └── test_products.py             # Pruebas unitarias
│
├── requirements.txt                 # Librerías a instalar
└── README.md
```

---

## Stack Tecnológico

| Tecnología | Uso |
|-------------|-----|
| **FastAPI** | Framework web principal |
| **Pydantic** | Validación y serialización de modelos |
| **Pytest** | Framework de testing |
| **Uvicorn** | Servidor ASGI |
| **JSON** | Persistencia local (mock de BD) |
| **Logging** | Seguimiento y depuración |

---

## Ejecución local

### 1. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Crear Archivo de variables de entorno

```bash
cp .env.example .env    #Ajustar valores si es necesario
```

### 4. Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

La API estará disponible en: <http://localhost:8000>

### 5. Ver documentación

- **Swagger UI → <http://localhost:8000/docs>**
- **ReDoc → <http://localhost:8000/redoc>**

---

## Modelo y Ejemplo de producto

### Modelo

| Campo           | Tipo                        | Requerido | Descripción                                                                        |
| --------------- | --------------------------- | --------- | ---------------------------------------------------------------------------------- |
| **id**          | `int`                       | Sí        | Identificador único del producto.                                                  |
| **name**        | `str`                       | Sí        | Nombre del producto.                                                               |
| **description** | `str`                       | Sí        | Descripción breve del producto.                                                    |
| **image_url**   | `HttpUrl`                   | Sí        | URL de la imagen del producto.                                                     |
| **price**       | `float`                     | Sí        | Precio del producto (mayor que 0).                                                 |
| **rating**      | `int` (opcional)            | No        | Calificación del producto (0 a 5). Por defecto (Null)                              |
| **specs**       | `dict[str, str]` (opcional) | No        | Especificaciones técnicas (pantalla, chip, cámara, batería, etc.).Por defecto ({}) |

### Ejemplo

```json
{
    "id": 1,
    "name": "iPhone 17 Pro",
    "description": "Smartphone Apple con chip A19 Bionic, cámara triple de 48 MP y pantalla Super Retina XDR de 6.7 pulgadas.",
    "image_url": "https://example.com/iphone17pro.jpg",
    "price": 4599.0,
    "rating": 5,
    "specs": {
      "screen": "6.7'' OLED 120Hz",
      "chip": "Apple A19 Bionic",
      "storage": "256 GB",
      "camera": "48 MP + 12 MP + 12 MP",
      "battery": "4500 mAh",
      "os": "iOS 18"
    }
},
```

---

## Endpoints principales

| Método   | Endpoint             | Descripción                | Respuesta esperada        |
| -------- | -------------------- | -------------------------- | ------------------------- |
| `GET`    | `/`                  | Health Check               | `200 OK` → `String`       |
| `GET`    | `/api/products/`     | Lista todos los productos  | `200 OK` → `[Product]`    |
| `GET`    | `/api/products/{id}` | Obtiene un producto por ID | `200 OK` → `Product`      |
| `POST`   | `/api/products/`     | Crea un nuevo producto     | `201 Created` → `Product` |
| `PUT`    | `/api/products/{id}` | Actualización completa     | `200 OK` → `Product`      |
| `PATCH`  | `/api/products/{id}` | Actualización parcial      | `200 OK` → `Product`      |
| `DELETE` | `/api/products/{id}` | Elimina un producto        | `204 No Content`          |

---

## Manejo de errores

| Código | Descripción                    | Ejemplo de respuesta                            |
| ------ | ------------------------------ | ----------------------------------------------- |
| `404`  | Producto no encontrado         | `{ "detail": "Product with id=123 not found" }` |
| `500`  | Error interno / archivo dañado | `{ "detail": "Error information" }`             |
| `422`  | Error de validación            | `{ "detail": [{"loc": ["string",0], "msg": "string", "type": "string" "input": "string", "ctx": {"expected_schemes": "string"}}]}`|

---

## Estrategia técnica

El proyecto sigue una arquitectura por capas, separando responsabilidades claramente:

- Modelos → validan estructura de datos y definen contratos.
- Servicios → encapsulan la lógica de negocio (lectura/escritura del JSON, validaciones, excepciones).
- Rutas → exponen los endpoints HTTP y gestionan respuestas estandarizadas.
- Tests → validan todas las operaciones posibles con fixtures aislados.

Además:

- Los logs siguen un flujo informativo → warning → error.

---

## Testing y cobertura

### Ejecutar test

```bash
pytest -v
```

### Coverage

```bash
pytest --cov=app --cov-report=term-missing
```

---

## Autor

**William Bernal**
Software Engineer | Senior Full Stack Developer & Technical Leader
Email → <willtf.wb@gmail.com>
LinkedIn → <https://www.linkedin.com/in/william-bernal-full-stack/>
