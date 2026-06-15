from conexionSQL import get_connection
from validacion_datos import pedir_entero, pedir_texto_obligatorio
def login():

    documento = pedir_texto_obligatorio("Documento: ")
    contrasena = pedir_entero("Contraseña: ")

    conexion = get_connection()
    cursor = conexion.cursor()

    #Consulta en SQL para determinar el rol del usuario.
    #Busca el docuemnto y la contra en todas las tablas
    busca_usuario = True

    while busca_usuario == True:
        sql = """
                SELECT documento, nombre, apellido
                FROM estudiantes
                WHERE documento = %s
                AND contrasena = %s
            """

        cursor.execute(sql, (documento, contrasena))
        if documento ==

    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    return resultado