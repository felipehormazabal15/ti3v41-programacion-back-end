PLAN DEL PROYECTO — SISTEMA DE PRÉSTAMO DE NOTEBOOKS

## 1. NEGOCIO

### Problema

En un laboratorio de computación puede ser necesario controlar si una persona cumple las condiciones básicas para solicitar un notebook. Actualmente, realizar esta comprobación manualmente puede provocar errores al revisar la edad de la persona o la cantidad de notebooks disponibles.

### Solución

El programa permitirá ingresar la edad de una persona y la cantidad de notebooks disponibles. Con esos datos determinará si el préstamo es aceptado, rechazado por edad, rechazado por falta de notebooks o si existe un dato inválido.

### Alcance

El programa solamente comprobará la condición de préstamo utilizando la edad y la cantidad de notebooks disponibles. Guardará los resultados en un archivo JSON y posteriormente los mostrará mediante una página web desarrollada con Django.

No se incluye una base de datos, sistema de usuarios, inicio de sesión, API ni gestión completa de inventario.

### Priorización MoSCoW

#### Must
- Solicitar la edad de la persona.
- Solicitar la cantidad de notebooks disponibles.
- Determinar el resultado del préstamo según las condiciones establecidas.
- Guardar los resultados en un archivo JSON.
- Mostrar los resultados mediante una página web en Django.

#### Should
- Permitir corregir un registro ingresado incorrectamente.
- Mostrar mensajes más detallados para cada resultado.

#### Could
- Permitir exportar los registros a otro formato.
- Incorporar un resumen de los préstamos.

#### Won't
- Sistema de usuarios y contraseñas.
- Base de datos.
- API.
- Sistema completo de administración de inventario.


## 2. TÉCNICO

### Datos de entrada

El programa solicitará dos datos:

- Edad: número entero.
- Cantidad de notebooks disponibles: número entero.

### Regla de decisión

El programa tendrá cuatro resultados:

1. Aceptado: ocurre cuando la edad es igual o mayor a 18 años y existe al menos un notebook disponible.
2. Rechazado por edad: ocurre cuando la persona es menor de 18 años.
3. Rechazado por falta de notebooks: ocurre cuando la persona tiene la edad requerida, pero no existen notebooks disponibles.
4. Dato inválido: ocurre cuando la cantidad de notebooks disponibles es menor que cero.

### Paquete externo

Se utilizará el paquete externo `tabulate` para mostrar los registros almacenados en JSON como una tabla ordenada en la consola.

### Pantalla web

La aplicación Django tendrá una sola pantalla accesible mediante una dirección web. La pantalla mostrará los registros almacenados en `datos.json`, incluyendo los datos ingresados y el resultado obtenido.
