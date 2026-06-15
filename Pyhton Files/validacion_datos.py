# Funciones para validar

def pedir_texto_obligatorio(mensaje):
    # Pide un texto por consola y valida que no esté vacío.
    num = "0123456789"
    while True:
        valor = input(mensaje).strip()
        contiene_num = False
        for letra in valor:
            if letra in num:
                contiene_num = True
                break
        if contiene_num == True:
            print("Error: El texto solicitado no puede contner números")
            continue

        if valor != "":
            return valor

        print("Error. Este campo no puede estar vacío.")


def pedir_entero(mensaje):

    while True:
        valor = input(mensaje).strip()

        if valor.isdigit():
            return int(valor)

        print("Error: debe ingresar un número válido.")


def pedir_entero_positivo(mensaje):
    # Pide un número entero mayor que cero.
    while True:
        numero = pedir_entero(mensaje)

        if numero > 0:
            return numero

        print("Error: el número debe ser mayor que cero.")


def pedir_opcion_valida(mensaje, opciones_validas):
    # Pide un texto y valida que esté dentro de una lista de opciones permitidas.
    while True:
        valor = input(mensaje).strip().lower()

        if valor in opciones_validas:
            return valor

        print("Error: opción inválida.")
        print("Opciones válidas:", ", ".join(opciones_validas))


def pedir_bool(mensaje):
    # Pide si/no por consola y luego lo convierte a True o False
    while True:
        valor = input(mensaje).strip().lower() #si hay espacios en blanco (antes y/o dsp) y en minuscula

        if valor == "":
            print("Error. Este campo no puede estar vacío.")
        elif valor == "si":
            return True
        elif valor == "no":
            return False
        else:
            print("Error. Ingrese un valor válido.")

def pedir_cedula(mensaje):
    # Pide un número entero de 8 digitos mayor que cero.
    while True:
        numero = pedir_entero(mensaje)

        if numero > 0 and len(str(numero))==8: #pasamos a str para contar digitos
            return numero

        print("Error: el documento tiene que tener 8 dígitos.")

def presione_enter():
    input("\nPresione Enter para continuar...")
