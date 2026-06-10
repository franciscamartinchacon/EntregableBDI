# Funciones para validar

def pedir_texto_obligatorio(mensaje):
    # Pide un texto por consola y valida que no esté vacío.
    while True:
        valor = input(mensaje).strip()

        if valor != "":
            return valor

        print("Error. Este campo no puede estar vacío.")


def pedir_entero(mensaje):

    while True:
        valor = input(mensaje).strip()

        if valor.isdigit():
            return int(valor)

        print("Error: debe ingresar un número válido.")

#normalizar datos???