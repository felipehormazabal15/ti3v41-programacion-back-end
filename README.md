# API REST - Sistema de Préstamo de Notebooks

## Descripción

Este proyecto corresponde a la evolución del sistema de préstamo de notebooks desarrollado en ES2.

En esta etapa se incorporó Django REST Framework (DRF) para exponer una API REST que utiliza los mismos modelos y la misma base de datos del proyecto Django.

Las vistas HTML originales de ES2 se mantienen funcionando en paralelo con la API.

## Tecnologías

* Python
* Django
* Django REST Framework
* SQLite
* TokenAuthentication

## Configuración de Django REST Framework

La API utiliza la siguiente configuración:

* `TokenAuthentication`: permite autenticar las solicitudes mediante un token enviado en la cabecera HTTP.
* `IsAuthenticated`: protege los endpoints para que no puedan utilizarse sin autenticación.
* `PageNumberPagination`: permite dividir los resultados en páginas.
* `PAGE_SIZE = 10`: limita cada página a 10 registros para evitar respuestas demasiado grandes.

Se eligió `TokenAuthentication` porque la API necesita que cada solicitud incluya una credencial de autenticación y permite mantener separada la autenticación de la sesión utilizada por las vistas HTML de ES2.

Se eligió una paginación de 10 registros por página para controlar el tamaño de las respuestas cuando aumente la cantidad de préstamos almacenados.

## Autenticación

Primero se debe obtener un token mediante:

`POST /api/token/`

Ejemplo:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"usuario_normal","password":"CONTRASEÑA"}'
```

El token debe enviarse en las solicitudes mediante el encabezado:

```text
Authorization: Token <TOKEN>
```

El token no debe escribirse directamente en el código ni incluirse en las URL.

## Endpoint principal

La API utiliza el recurso plural:

`/api/prestamos/`

No se utilizan verbos dentro de las URL. La operación se determina mediante el método HTTP.

| Método | Endpoint               | Descripción                         | Respuesta |
| ------ | ---------------------- | ----------------------------------- | --------- |
| GET    | `/api/prestamos/`      | Lista los préstamos                 | 200       |
| POST   | `/api/prestamos/`      | Crea un préstamo                    | 201       |
| GET    | `/api/prestamos/<id>/` | Obtiene un préstamo                 | 200       |
| PUT    | `/api/prestamos/<id>/` | Actualiza completamente un préstamo | 200       |
| PATCH  | `/api/prestamos/<id>/` | Actualiza parcialmente un préstamo  | 200       |
| DELETE | `/api/prestamos/<id>/` | Elimina lógicamente un préstamo     | 204       |

## Permisos

Los permisos de la API mantienen la lógica de roles utilizada en ES2.

| Rol    | GET | POST | PUT/PATCH | DELETE |
| ------ | --: | ---: | --------: | -----: |
| viewer |  Sí |   No |        No |     No |
| normal |  Sí |   Sí |        No |     No |
| admin  |  Sí |   Sí |        Sí |     Sí |

Los usuarios deben estar autenticados para acceder a la API.

Una solicitud sin token devuelve `401 Unauthorized`.

Un usuario autenticado que no posee permisos para realizar una operación recibe `403 Forbidden`.

## Serializer

El recurso `PrestamoNotebook` utiliza `PrestamoNotebookSerializer`.

Los campos expuestos por la API son:

* `id`
* `nombre`
* `edad`
* `cupos_disponibles`
* `estado`
* `motivo`
* `creado_en`
* `eliminado`
* `fecha_eliminacion`

Los siguientes campos son de solo lectura:

* `id`
* `estado`
* `motivo`
* `creado_en`
* `eliminado`
* `fecha_eliminacion`

`estado` y `motivo` no son enviados por el usuario. Son calculados por el backend mediante la regla de negocio existente en `services.py`.

## Validaciones

El serializer valida:

* Que el nombre no esté vacío.
* Que la cantidad de notebooks no sea negativa.

Por ejemplo, un `POST` con `cupos_disponibles = -1` devuelve:

`400 Bad Request`

con un mensaje JSON indicando el error.

La edad menor de 18 años no se considera un dato inválido. Es una condición de negocio que produce el estado `RECHAZADO`.

## Paginación

La API utiliza paginación por número de página con un máximo de 10 registros por página.

La respuesta contiene:

* `count`
* `next`
* `previous`
* `results`

Ejemplo:

```json
{
    "count": 11,
    "next": "http://127.0.0.1:8000/api/prestamos/?page=2",
    "previous": null,
    "results": []
}
```

## Códigos HTTP utilizados

* `200 OK`: consulta o modificación exitosa.
* `201 Created`: recurso creado correctamente.
* `204 No Content`: eliminación correcta.
* `400 Bad Request`: datos inválidos.
* `401 Unauthorized`: falta autenticación.
* `403 Forbidden`: usuario autenticado sin permisos suficientes.
* `404 Not Found`: recurso inexistente.

## Pruebas realizadas

Se realizaron pruebas con `curl` para comprobar:

* Acceso sin token.
* Acceso con token.
* Permisos del usuario `normal`.
* Permisos del usuario `admin`.
* Creación de préstamos.
* Consulta de préstamos.
* Consulta de un préstamo específico.
* Modificación parcial mediante `PATCH`.
* Eliminación mediante `DELETE`.
* Validación de datos incorrectos.
* Consulta de recursos inexistentes.
* Paginación.

Las pruebas confirmaron respuestas `401`, `403`, `200`, `201`, `204`, `400` y `404` según cada situación.

## Lógica de negocio

La API reutiliza la función `evaluar_prestamo()` ubicada en `core/services.py`.

Las reglas principales son:

* Cupos negativos: dato inválido.
* Edad menor de 18 años: préstamo rechazado.
* Sin notebooks disponibles: préstamo rechazado.
* Edad suficiente y notebooks disponibles: préstamo aceptado.

La lógica se ejecuta automáticamente al crear o modificar un préstamo.

## Estructura relacionada con la API

```text
core/
├── api_views.py
├── permissions.py
├── serializers.py
├── services.py
└── models.py

config/
├── settings.py
└── urls.py
```

## Seguridad

La API utiliza autenticación mediante token y permisos diferenciados por rol.

Los tokens deben mantenerse fuera del código fuente y no deben incluirse en las URL.

El archivo `.env` tampoco debe incorporarse al repositorio.

## Ejemplos de respuestas

### Creación correcta

```json
{
    "id": 12,
    "nombre": "Prueba usuario normal",
    "edad": 20,
    "cupos_disponibles": 3,
    "estado": "ACEPTADO",
    "motivo": "La persona cumple la edad requerida y hay notebooks disponibles."
}
```

### Validación incorrecta

```json
{
    "cupos_disponibles": [
        "La cantidad de notebooks no puede ser negativa."
    ]
}
```

### Falta de autenticación

```json
{
    "detail": "Las credenciales de autenticación no se proveyeron."
}
```
