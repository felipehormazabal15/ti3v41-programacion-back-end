# Uso de Inteligencia Artificial

## Herramienta utilizada

Utilicé ChatGPT como herramienta de Inteligencia Artificial para recibir orientación durante el desarrollo del proyecto de Programación Back End.

La IA fue utilizada como apoyo para analizar los requerimientos de la Unidad 2, proponer soluciones, revisar errores y orientar las pruebas realizadas en el proyecto.

## Consultas realizadas

Una de las consultas principales fue solicitar ayuda paso a paso para implementar los requerimientos de la Unidad 2, manteniendo la regla de decisión original del proyecto y evitando duplicar la lógica.

También realicé consultas relacionadas con:

- Configuración de SQLite y del modelo `PrestamoNotebook`.
- Creación y aplicación de migraciones.
- Configuración del panel de administración de Django.
- Implementación de las operaciones CRUD.
- Reutilización de la regla de decisión mediante `services.py`.
- Implementación del borrado lógico.
- Implementación de login y logout.
- Creación de los roles `admin`, `normal` y `viewer`.
- Configuración de contraseñas mediante `.env`.
- Configuración de `.gitignore` y `.env.example`.
- Implementación de mensajes de confirmación.
- Creación de pruebas en `core/tests.py`.
- Revisión de errores durante las pruebas.

## Sugerencias de IA que fueron adoptadas

Después de revisar las sugerencias y comprobarlas en el proyecto, adopté varias de ellas:

- Utilizar SQLite como base de datos.
- Crear el modelo `PrestamoNotebook`.
- Utilizar migraciones de Django para crear y modificar la estructura de la base de datos.
- Separar la regla de decisión en `services.py` para reutilizarla al crear y editar.
- Implementar las operaciones CRUD mediante vistas, rutas y formularios.
- Utilizar borrado lógico mediante `eliminado` y `fecha_eliminacion`.
- Utilizar el sistema de autenticación incorporado de Django.
- Controlar los roles mediante grupos y un decorador propio.
- Utilizar variables de entorno para las contraseñas de prueba.
- Utilizar mensajes de Django para informar al usuario después de las operaciones.

## Revisión crítica y correcciones

Las sugerencias de la IA no fueron aplicadas sin comprobarlas. Durante el desarrollo encontré situaciones que tuve que revisar y corregir.

Por ejemplo:

- El primer intento de cerrar sesión mediante una solicitud GET produjo un error `405 Method Not Allowed`. Se corrigió utilizando un formulario POST con protección CSRF, de acuerdo con el funcionamiento esperado de Django.
- La plantilla `resumen.html` tuvo contenido duplicado y texto de formato Markdown. Se reemplazó por una plantilla HTML limpia.
- Los mensajes de confirmación se agregaron primero en las vistas, pero después fue necesario revisar la plantilla para mostrar realmente los mensajes al usuario.
- Al implementar la creación automática de grupos se detectó que no era conveniente registrar dos veces la misma señal `post_migrate`. Se revisó la configuración para evitar una conexión duplicada.
- El grupo personalizado `admin` no otorgaba por sí solo acceso al panel `/admin/` de Django. Para la cuenta de administración utilizada en las pruebas fue necesario configurar los permisos propios del sistema de administración de Django.
- Las pruebas del proyecto mostraron inicialmente que `core/tests.py` estaba vacío. Se agregaron pruebas para comprobar el CRUD y las restricciones de los roles.

## Verificación de las sugerencias

Las modificaciones propuestas fueron comprobadas mediante diferentes verificaciones:

- `python manage.py check`
- `python manage.py makemigrations --check --dry-run`
- `python manage.py migrate`
- Pruebas manuales de login y logout.
- Pruebas manuales de los roles `admin`, `normal` y `viewer`.
- Pruebas del panel de administración.
- Pruebas del borrado lógico.
- Pruebas de creación, edición y eliminación.
- `python manage.py test`

Las pruebas automatizadas terminaron correctamente con:

`Found 6 test(s).`

`Ran 6 tests`

`OK`

La herramienta de IA fue utilizada como apoyo y orientación. Las decisiones finales, modificaciones, configuraciones y pruebas fueron revisadas y realizadas en mi propio proyecto.
# Uso de Inteligencia Artificial - ES3

## Uso de IA durante la implementación de la API REST

Durante la ES3 utilicé ChatGPT como apoyo para transformar el proyecto Django de ES2 en una API REST utilizando Django REST Framework.

Las consultas estuvieron relacionadas con:

* Configuración de `rest_framework` y `rest_framework.authtoken`.
* Configuración de `REST_FRAMEWORK` en `settings.py`.
* Creación de `ModelSerializer`.
* Creación de `ModelViewSet`.
* Configuración de `DefaultRouter`.
* Implementación de autenticación mediante tokens.
* Creación de permisos diferenciados para los grupos `admin`, `normal` y `viewer`.
* Validaciones de los datos enviados mediante JSON.
* Uso correcto de códigos HTTP.
* Paginación de resultados.
* Documentación de los endpoints en `README.md`.
* Pruebas de la API utilizando `curl`.

## Consulta crítica sobre seguridad

Una consulta realizada fue cómo proteger los endpoints de la API mediante Django REST Framework y cómo evitar que una implementación recomendada por una IA dejara la API expuesta.

Se revisaron especialmente las siguientes posibilidades:

* Utilizar `AllowAny`.
* Colocar el token directamente en el código.
* Enviar el token como parte de la URL.
* Utilizar `fields = "__all__"` en el serializer.
* Desactivar protecciones de Django mediante `csrf_exempt` sin una justificación.

Estas alternativas no fueron utilizadas porque podían reducir la seguridad de la aplicación o exponer información innecesariamente.

En su lugar se utilizó:

* `TokenAuthentication`.
* `IsAuthenticated` como permiso predeterminado.
* Una clase de permisos propia para diferenciar las operaciones según el grupo del usuario.
* Campos explícitos en el serializer.
* El encabezado `Authorization: Token <TOKEN>` para enviar las credenciales.

## Ejemplo de una recomendación revisada y corregida

Durante la implementación del serializer se revisó la validación de la edad.

Una primera posibilidad era validar directamente que la edad fuera igual o mayor a 18 años dentro del serializer.

Esta solución no era adecuada para este proyecto porque la edad menor de 18 años forma parte de la regla de negocio existente en `services.py`. Según la lógica del sistema, una persona menor de 18 años no representa un dato inválido: corresponde al estado `RECHAZADO`.

Por esta razón se descartó esa validación en el serializer.

El serializer quedó encargado de validar los datos estructurales, como que los cupos no sean negativos, mientras que `evaluar_prestamo()` mantiene la decisión de negocio.

Esto fue comprobado mediante una prueba:

* Edad: `17`
* Cupos: `3`
* Resultado HTTP: `201 Created`
* Estado calculado: `RECHAZADO`
* Motivo: `La persona es menor de 18 años.`

## Ejemplo de permisos diferenciados

También se revisó la posibilidad de permitir todas las operaciones a cualquier usuario autenticado.

Esta alternativa fue descartada porque no respetaba los roles definidos en el proyecto.

La implementación final diferencia las operaciones:

* `viewer`: puede consultar.
* `normal`: puede consultar y crear.
* `admin`: puede consultar, crear, modificar y eliminar.

Las pruebas confirmaron que:

* Un usuario sin grupo no pudo crear y recibió `403 Forbidden`.
* Un usuario `normal` pudo crear un préstamo y recibió `201 Created`.
* Un usuario `normal` no pudo modificar un préstamo y recibió `403 Forbidden`.
* Un usuario `admin` pudo modificar y recibió `200 OK`.
* Un usuario `normal` no pudo eliminar y recibió `403 Forbidden`.
* Un usuario `admin` pudo eliminar y recibió `204 No Content`.

## Verificación de la API

Las recomendaciones y modificaciones fueron comprobadas mediante pruebas reales del proyecto.

Entre las respuestas verificadas se encuentran:

* `401 Unauthorized`: solicitud sin token.
* `403 Forbidden`: usuario autenticado sin permisos suficientes.
* `200 OK`: consulta y modificación correcta.
* `201 Created`: creación correcta.
* `204 No Content`: eliminación lógica correcta.
* `400 Bad Request`: datos inválidos.
* `404 Not Found`: recurso inexistente.

También se verificó la paginación de los resultados, obteniendo 10 registros por página.

## Decisiones finales

La IA fue utilizada como apoyo para analizar alternativas y resolver problemas, pero sus sugerencias fueron revisadas antes de incorporarlas al proyecto.

Las decisiones finales fueron:

* Mantener las vistas HTML de ES2.
* Incorporar la API en paralelo bajo `/api/`.
* Utilizar `ModelSerializer` con campos explícitos.
* Mantener `estado` y `motivo` como campos de solo lectura.
* Utilizar `ModelViewSet` y `DefaultRouter`.
* Proteger la API mediante autenticación por token.
* Implementar permisos diferenciados por rol.
* Reutilizar `evaluar_prestamo()` para mantener una sola regla de negocio.
* Utilizar códigos HTTP adecuados según el resultado de cada operación.
* Documentar la API en `README.md`.

La herramienta de IA fue utilizada como apoyo y orientación. Las decisiones finales, modificaciones y pruebas fueron revisadas y realizadas en mi propio proyecto.
