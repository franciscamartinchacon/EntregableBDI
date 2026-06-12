from conexionSQL import get_connection

def login():

    usuario = input("Uusuario: ")
    contrasena = input("Contraseña: ")

    conexion = get_connection()
    cursor = conexion.cursor()

    #Consulta en SQL para determinar el rol del usuario.
    sql = """
            SELECT documento, rol
            FROM usuarios
            WHERE nombre_usuario = %s
            AND contrasena = %s
        """

    cursor.execute(sql, (usuario, contrasena))

    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    return resultado