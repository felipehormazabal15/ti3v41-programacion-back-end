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
