**DOCUMENTACIÓN E INSTRUCTIVO PARA CORRER LA APLICACIÓN LOCALMENTE**

Entregable Base de Datos I - Francisca Martin y Sofía Mazzilli

**Antes de correr la aplicación:**

Para poder ejecutar la aplicación localmente, es necesario tener instalado:

- Python
- MySQL Server
- PyCharm (editor de código)
- DataGrip (gestor de base de datos)
- La librería mysql-connector-python

La librería se instala desde la terminal con el siguiente comando: 

pip install mysql-connector-python

**Crear base de datos**

Antes de ejecutar el programa en Python, se debe crear la base de datos en MySQL.

Ejecutar **archivo SQL** desde DataGrip

**¿Qué hace?**

- Elimina la base anterior si existe para evitar errores.
- Crea la base de datos **entregablebd1**.
- Crea las tablas necesarias.
- Carga datos iniciales de prueba.

**Abrir el programa en PyCharm**

1. Configurar la conexión a MySQL desde PyCharm

El archivo _conexionSQL.py_ contiene la función que permite conectar Python con MySQL.

Antes de ejecutar el sistema, verificar que los datos de conexión coincidan con los de la computadora local.

-> Revisar host, user y password. 

2. Ejecutar _main.py_
   
4. Iniciar sesión

El sistema permite ingresar como:

- Administrador
- Docente
- Estudiante
  
-> Según el rol, las funcionalidades disponibles

**Usuarios de prueba:**

-> *Administrador:*

  Documento: 56082008

  Contraseña: admin1



-> *Docente:*

  Documento: 55711122

  Contraseña: laura123


-> *Estudiante:*

  Documento: 55511122

  Contraseña: ana123
  

**Funcionamiento general**

La aplicación funciona mediante menús por consola.

Para seleccionar una opción, se debe ingresar el número correspondiente y presionar Enter.
