PLAN DEL PROYECTO — SISTEMA DE PRÉSTAMO DE NOTEBOOKS

## 1. NEGOCIO

### Problema

En un laboratorio de computación puede ser necesario controlar si una persona cumple las condiciones básicas para solicitar un notebook. Actualmente, realizar esta comprobación manualmente puede provocar errores al revisar la edad de la persona o la cantidad de notebooks disponibles.

### Solución

El sistema permitirá ingresar la edad de una persona y la cantidad de notebooks disponibles. Con esos datos determinará si el préstamo es aceptado, rechazado por edad, rechazado por falta de notebooks o si existe un dato inválido.

Los registros serán almacenados en una base de datos SQLite y podrán ser gestionados mediante una aplicación web desarrollada con Django.

### Alcance

El sistema comprobará la condición de préstamo utilizando la edad y la cantidad de notebooks disponibles.

Los registros se almacenarán en SQLite y podrán ser consultados, creados, actualizados y eliminados mediante operaciones CRUD.

El sistema también contará con inicio de sesión y roles de usuario:
- `admin`: puede crear, editar y eliminar registros.
- `normal`: puede crear registros y consultar.
- `viewer`: puede consultar registros.

La eliminación de registros será lógica, manteniendo el registro en la base de datos y marcándolo como eliminado.

No se incluye una API ni una gestión completa de inventario.

### Priorización MoSCoW

#### Must
- Solicitar la edad de la persona.
- Solicitar la cantidad de notebooks disponibles.
- Determinar el resultado del préstamo según las condiciones establecidas.
- Utilizar SQLite como base de datos.
- Permitir consultar los registros.
- Permitir crear registros.
- Permitir actualizar registros.
- Permitir eliminar registros mediante borrado lógico.
- Implementar inicio de sesión.
- Implementar los roles `admin`, `normal` y `viewer`.
- Controlar los permisos de los usuarios según su rol.

#### Should
- Permitir corregir un registro ingresado incorrectamente.
- Mostrar mensajes más detallados para cada resultado.
- Administrar los registros mediante el panel de administración de Django.

#### Could
- Permitir exportar los registros a otro formato.
- Incorporar un resumen de los préstamos.

#### Won't
- API.
- Sistema completo de administración de inventario.

## 2. TÉCNICO

### Datos de entrada

El sistema utilizará los siguientes datos:

- Nombre: texto.
- Edad: número entero.
- Cantidad de notebooks disponibles: número entero.

### Regla de decisión

El sistema tendrá cuatro resultados:

1. Aceptado: ocurre cuando la edad es igual o mayor a 18 años y existe al menos un notebook disponible.
2. Rechazado por edad: ocurre cuando la persona es menor de 18 años.
3. Rechazado por falta de notebooks: ocurre cuando la persona tiene la edad requerida, pero no existen notebooks disponibles.
4. Dato inválido: ocurre cuando la cantidad de notebooks disponibles es menor que cero.

La regla de decisión será reutilizada al crear y actualizar registros.

### Base de datos

Se utilizará SQLite para almacenar los registros de préstamos.

El modelo `PrestamoNotebook` almacenará los datos de cada registro, incluyendo el nombre, edad, cupos disponibles, estado, motivo y fecha de creación.

Para el borrado lógico se utilizarán los campos `eliminado` y `fecha_eliminacion`.

### CRUD

La aplicación contará con cuatro operaciones principales:

- Crear: registrar un nuevo préstamo.
- Leer: consultar los préstamos registrados.
- Actualizar: modificar un registro existente y recalcular su estado.
- Eliminar: marcar un registro como eliminado sin borrarlo físicamente de la base de datos.

### Autenticación y roles

El sistema utilizará el sistema de autenticación de Django para el inicio y cierre de sesión.

Se utilizarán tres roles:

- `admin`: puede crear, editar y eliminar.
- `normal`: puede crear y consultar.
- `viewer`: puede consultar.

Los permisos serán controlados desde el servidor.

### Pantalla web

La aplicación Django permitirá iniciar sesión y acceder a la pantalla de préstamos según el rol del usuario.

La pantalla mostrará los registros activos almacenados en SQLite y permitirá realizar las operaciones correspondientes según los permisos del usuario.