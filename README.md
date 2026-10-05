# API REST - Sistema de Préstamo de Notebooks

## Descripción

Este proyecto corresponde a la evolución del sistema de préstamo de notebooks desarrollado en ES2.

En esta etapa se incorporó Django REST Framework (DRF) para exponer una API RESTful que utiliza los mismos modelos y la misma base de datos del proyecto.

Las vistas HTML originales de ES2 se mantienen funcionando en paralelo con la API.

## Tecnologías

* Python
* Django
* Django REST Framework
* djangorestframework-simplejwt
* SQLite

## Configuración de Django REST Framework

La API utiliza la siguiente configuración:

* `JWTAuthentication`: permite autenticar las solicitudes mediante tokens JWT enviados en la cabecera HTTP.
* `IsAuthenticated`: protege los endpoints para que no puedan utilizarse sin autenticación.
* `PageNumberPagination`: permite dividir los resultados en páginas.
* `PAGE_SIZE = 10`: limita cada página a 10 registros para controlar el tamaño de las respuestas.

Se eligió `JWTAuthentication` porque la API necesita proteger sus endpoints mediante credenciales y, además, se requiere controlar la duración de los tokens. Se configuró un access token con una duración de 30 minutos y un refresh token con una duración de 1 día. Esto reduce el tiempo de exposición del access token y permite obtener uno nuevo mediante el refresh token sin solicitar nuevamente las credenciales.

Se eligió una paginación de 10 registros por página para controlar el tamaño de las respuestas y evitar entregar demasiados registros en una sola solicitud.

## Autenticación JWT

La API utiliza JSON Web Tokens (JWT) para autenticar las solicitudes.

### Obtener tokens

Para obtener un access token y un refresh token se utiliza:

```text
POST /api/token/
```

Ejemplo:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
-H "Content-Type: application/json" \
-d '{"username":"usuario_normal","password":"CONTRASEÑA"}'
```

La respuesta contiene:

```json
{
    "refresh": "<REFRESH_TOKEN>",
    "access": "<ACCESS_TOKEN>"
}
```

El access token tiene una duración de 30 minutos.

El refresh token tiene una duración de 1 día.

### Renovar el access token

Cuando el access token expira, se puede solicitar uno nuevo utilizando el refresh token:

```text
POST /api/token/refresh/
```

Ejemplo:

```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
-H "Content-Type: application/json" \
-d '{"refresh":"<REFRESH_TOKEN>"}'
```

### Autenticar solicitudes

Las solicitudes protegidas deben enviar el access token mediante la cabecera HTTP:

```text
Authorization: Bearer <ACCESS_TOKEN>
```

El token no se incluye en la URL ni se almacena directamente en el código fuente.

## Endpoints REST

La API utiliza URLs basadas en recursos y métodos HTTP para indicar la operación.

| Método | URL | Descripción | Autenticación |
|---|---|---|---|
| GET | `/api/prestamos/` | Lista préstamos no eliminados | JWT |
| POST | `/api/prestamos/` | Crea un préstamo | JWT |
| GET | `/api/prestamos/<id>/` | Obtiene un préstamo específico | JWT |
| PUT | `/api/prestamos/<id>/` | Actualiza completamente un préstamo | JWT + admin |
| PATCH | `/api/prestamos/<id>/` | Actualiza parcialmente un préstamo | JWT + admin |
| DELETE | `/api/prestamos/<id>/` | Elimina lógicamente un préstamo | JWT + admin |
| POST | `/api/token/` | Obtiene access y refresh token | Credenciales |
| POST | `/api/token/refresh/` | Obtiene un nuevo access token | Refresh token |

Se utilizan nombres de recursos en plural, como `/api/prestamos/`, y las operaciones se realizan mediante los métodos HTTP correspondientes.

## Permisos

La API utiliza permisos diferenciados según el grupo del usuario.

| Usuario | GET | POST | PUT/PATCH | DELETE |
|---|---:|---:|---:|---:|
| Usuario del grupo `viewer` | Sí | No | No | No |
| Usuario del grupo `normal` | Sí | Sí | No | No |
| Usuario del grupo `admin` | Sí | Sí | Sí | Sí |

Todos los endpoints de préstamos requieren autenticación mediante JWT.

Los usuarios del grupo `normal` pueden consultar y crear préstamos.

Los usuarios del grupo `admin` pueden consultar, crear, modificar y eliminar lógicamente préstamos.

## Serializador

El serializador utilizado es:

```text
PrestamoNotebookSerializer
```

Los campos expuestos por la API son:

```text
id
nombre
edad
cupos_disponibles
estado
motivo
creado_en
eliminado
fecha_eliminacion
```

Los siguientes campos son de solo lectura:

```text
id
estado
motivo
creado_en
eliminado
fecha_eliminacion
```

El estado y el motivo no pueden ser enviados libremente por el cliente, ya que son determinados por la lógica de negocio.

No se utiliza `fields = "__all__"` para mantener explícitamente controlados los campos que la API expone.

## Validaciones

El serializador realiza validaciones antes de guardar los datos.

El nombre no puede estar vacío.

La cantidad de notebooks no puede ser negativa.

Ejemplo de respuesta ante una validación incorrecta:

```json
{
    "cupos_disponibles": [
        "La cantidad de notebooks no puede ser negativa."
    ]
}
```

La lógica de negocio se mantiene centralizada en:

```text
core/services.py
```

mediante la función:

```text
evaluar_prestamo()
```

Esta función determina el estado y motivo del préstamo según la edad y los cupos disponibles.

## Paginación

La API utiliza:

```text
PageNumberPagination
```

con:

```text
PAGE_SIZE = 10
```

Una respuesta de listado puede tener la siguiente estructura:

```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": []
}
```

## Códigos de respuesta HTTP

La API utiliza códigos HTTP según el resultado de cada operación:

| Código | Significado |
|---|---|
| 200 | Solicitud exitosa |
| 201 | Recurso creado correctamente |
| 204 | Recurso eliminado correctamente |
| 400 | Datos enviados no válidos |
| 401 | Falta autenticación o el token no es válido |
| 403 | Usuario autenticado pero sin permisos suficientes |
| 404 | Recurso no encontrado |

## Eliminación lógica

Los préstamos no se eliminan físicamente de la base de datos.

La API utiliza una eliminación lógica mediante los campos:

```text
eliminado
fecha_eliminacion
```

Cuando se utiliza `DELETE`, el registro se marca como eliminado.

Los registros eliminados no aparecen en el listado principal de:

```text
GET /api/prestamos/
```

## Pruebas realizadas

Las pruebas funcionales de la API se encuentran en la carpeta:

```text
pruebas/
```

Se verificaron, entre otros, los siguientes casos:

* Acceso sin autenticación.
* Acceso utilizando JWT.
* Permisos diferenciados por grupo.
* Creación de préstamos.
* Consulta de préstamos.
* Actualización de préstamos.
* Eliminación lógica.
* Recurso inexistente.
* Datos inválidos.
* Paginación.
* Obtención de access y refresh token.
* Renovación del access token mediante refresh token.

## Ejemplo de acceso autenticado

Una solicitud protegida utiliza:

```bash
curl -i \
-H "Authorization: Bearer <ACCESS_TOKEN>" \
http://127.0.0.1:8000/api/prestamos/
```

Una solicitud correctamente autenticada puede responder:

```text
HTTP/1.1 200 OK
```

## Estructura principal

```text
mi_proyecto/
├── config/
│   ├── settings.py
│   └── urls.py
├── core/
│   ├── api_views.py
│   ├── decorators.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── services.py
│   └── views.py
├── pruebas/
├── ia.md
├── manage.py
├── requirements.txt
└── README.md
```

## Seguridad

La API utiliza autenticación JWT para proteger los endpoints.

Los endpoints de préstamos requieren un usuario autenticado.

Los permisos se diferencian mediante los grupos `admin`, `normal` y `viewer`.

Los access tokens tienen una duración limitada de 30 minutos y los refresh tokens de 1 día.

Los tokens no se incluyen en las URLs ni se almacenan directamente en el código fuente.

No se utiliza `AllowAny` para los endpoints protegidos.

No se utiliza `csrf_exempt` para desactivar las protecciones de Django.

Los campos sensibles o internos no se exponen mediante `fields = "__all__"`.

## Lógica de negocio

La lógica para evaluar los préstamos se mantiene separada de las vistas mediante:

```text
core/services.py
```

La función:

```text
evaluar_prestamo()
```

determina el estado del préstamo:

* `ACEPTADO`
* `RECHAZADO`
* `INVALIDO`

La API reutiliza esta misma lógica tanto al crear como al actualizar un préstamo.

## Uso crítico de IA

La inteligencia artificial se utilizó como apoyo para comprender Django REST Framework, serializadores, ViewSets, routers, autenticación, permisos, códigos HTTP, paginación y documentación.

Las recomendaciones generadas por IA fueron revisadas y probadas antes de incorporarlas al proyecto.

No se aceptaron recomendaciones inseguras como utilizar `AllowAny` para endpoints protegidos, almacenar tokens en el código, enviar tokens mediante la URL, utilizar `fields = "__all__"` sin revisar los campos expuestos o desactivar CSRF mediante `csrf_exempt`.

Como parte de la revisión del proyecto se identificó que `TokenAuthentication` no permitía cumplir con el requisito de expiración de tokens. Por esta razón se reemplazó por `JWTAuthentication` mediante `djangorestframework-simplejwt`.

Se configuró un access token de 30 minutos y un refresh token de 1 día, decisión tomada para reducir la exposición del access token y permitir su renovación sin volver a ingresar las credenciales.

Las decisiones finales fueron comprobadas mediante pruebas funcionales de la API.

## Conclusión

La API REST permite gestionar los préstamos de notebooks utilizando Django REST Framework, manteniendo las vistas HTML originales de ES2.

La implementación incorpora serializadores explícitos, ViewSet, router, validaciones, paginación, permisos diferenciados, autenticación JWT con expiración y refresh tokens, códigos HTTP apropiados y eliminación lógica.

La API mantiene separada la presentación HTML de ES2 de los endpoints REST de ES3 y reutiliza la misma base de datos y lógica de negocio.
