# PROMPTS

## Contexto

Durante el desarrollo de la prueba técnica **Comparison API**, se utilizó asistencia con **IA generativa (ChatGPT - GPT-5)** únicamente como apoyo para acelerar la documentación, estructura base y validación de buenas prácticas de FastAPI.

## Uso de la IA

Las herramientas de IA se usaron en los siguientes puntos:

1. **Estructura inicial del proyecto**
   Se solicitó ayuda para definir una arquitectura limpia (capas: routes, models, services, utils).

2. **Buenas prácticas de documentación**
   La IA ayudó a redactar secciones del `README.md` y a uniformar el formato de la tabla de endpoints.

3. **Casos de prueba y cobertura**
   Se discutieron ideas para aislar correctamente los tests con `pytest` y `tmp_path`, garantizando cobertura total sin modificar el archivo real.

4. **Manejo de errores estandarizados**
   Se consultó sobre cómo representar respuestas `404`, `500` y `422` de forma consistente en Swagger (`responses_common`).

## Trabajo propio

- Todo el **código fuente (Python)** fue **escrito, adaptado y revisado manualmente**.
- Las pruebas (`test_products.py`), configuración de fixtures, permisos de archivo simulados y validaciones fueron diseñadas y ejecutadas por mí.
- Se logró **100% de cobertura** tras validación manual con `pytest --cov`.

## Reflexión

El uso de IA permitió mejorar la velocidad y estandarización del desarrollo, sin sustituir la comprensión técnica ni el razonamiento detrás de cada decisión de arquitectura o test.

---

**Autor:** William Bernal
**Herramienta utilizada:** ChatGPT (GPT-5)
