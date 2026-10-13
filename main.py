
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error,
    imprimir_info, confirmar
)

from views import (
    crear_estudiante, obtener_estudiantes, buscar_estudiantes,
    obtener_estudiante, actualizar_estudiante, eliminar_estudiante,
    crear_materia, obtener_materias, buscar_materias,
    obtener_materia, actualizar_materia, eliminar_materia,
    materias_sin_cupo, crear_matricula, obtener_matriculas,
    obtener_matricula, registrar_nota, retirar_matricula,
    certificado, promedio_de_estudiante
)


# =====================================================================
# AYUDAS DE PANTALLA
# =====================================================================

def pausa():
    input("\nPresione Enter para continuar...")


def pedir_entero(etiqueta):
    try:
        return int(input(etiqueta))
    except ValueError:
        imprimir_error("Debe ingresar un número entero.")
        return None


def mostrar_resultado(exito, mensaje):
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def mostrar_lista(objetos, vacio="No hay registros todavía."):
    if not objetos:
        imprimir_info(vacio)
        return

    for objeto in objetos:
        print(f"  {objeto}")

    imprimir_info(f"Total: {len(objetos)}")


def mostrar_detalle(objeto):
    for clave, valor in objeto.a_diccionario().items():
        nombre = str(clave).replace("_", " ").capitalize()
        print(f"  {nombre:<18}: {valor}")


# =====================================================================
# MENÚ DE ESTUDIANTES
# =====================================================================

def crear_estudiante_menu():
    imprimir_titulo("REGISTRAR ESTUDIANTE")

    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Correo electrónico: "),
        "carnet": input("Carnet: "),
        "carrera": input("Carrera: ")
    }

    mostrar_resultado(*crear_estudiante(datos))
    pausa()


def listar_estudiantes():
    imprimir_titulo("ESTUDIANTES")
    mostrar_lista(
        obtener_estudiantes(),
        "Todavía no hay estudiantes registrados."
    )
    pausa()


def buscar_estudiante_menu():
    imprimir_titulo("BUSCAR ESTUDIANTE")

    termino = input("Nombre, carnet, correo o carrera: ")

    encontrados = buscar_estudiantes(termino)

    mostrar_lista(encontrados, "No se encontraron estudiantes.")
    pausa()


def ver_estudiante():
    imprimir_titulo("CONSULTAR ESTUDIANTE")

    id_estudiante = pedir_entero("ID del estudiante: ")

    if id_estudiante is not None:
        estudiante = obtener_estudiante(id_estudiante)

        if estudiante is None:
            imprimir_error("Estudiante no encontrado.")
        else:
            mostrar_detalle(estudiante)

    pausa()


def actualizar_estudiante_menu():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")

    id_estudiante = pedir_entero("ID del estudiante: ")

    if id_estudiante is None:
        return pausa()

    estudiante = obtener_estudiante(id_estudiante)

    if estudiante is None:
        imprimir_error("Estudiante no encontrado.")
        return pausa()

    imprimir_info(f"Editando: {estudiante.etiqueta()}")
    print("Deje vacío un campo si no desea cambiarlo.\n")

    cambios = {}

    for campo in ("nombre", "apellido", "email", "carnet", "carrera"):
        actual = getattr(estudiante, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()

        if nuevo:
            cambios[campo] = nuevo

    if cambios:
        mostrar_resultado(
            *actualizar_estudiante(id_estudiante, cambios)
        )
    else:
        imprimir_info("No se realizaron cambios.")

    pausa()


def eliminar_estudiante_menu():
    imprimir_titulo("ELIMINAR ESTUDIANTE")

    id_estudiante = pedir_entero("ID del estudiante: ")

    if id_estudiante is None:
        return pausa()

    estudiante = obtener_estudiante(id_estudiante)

    if estudiante is None:
        imprimir_error("Estudiante no encontrado.")
        return pausa()

    imprimir_info(f"Se eliminará: {estudiante.etiqueta()}")

    if confirmar("¿Confirma la eliminación?"):
        mostrar_resultado(eliminar_estudiante(id_estudiante))
    else:
        imprimir_info("Operación cancelada.")

    pausa()


# =====================================================================
# MENÚ DE MATERIAS
# =====================================================================

def crear_materia_menu():
    imprimir_titulo("REGISTRAR MATERIA")

    datos = {
        "nombre": input("Nombre de la materia: "),
        "codigo": input("Código: "),
        "creditos": input("Número de créditos: "),
        "cupos": input("Cupos disponibles: ")
    }

    mostrar_resultado(*crear_materia(datos))
    pausa()


def listar_materias():
    imprimir_titulo("MATERIAS")

    mostrar_lista(
        obtener_materias(),
        "Todavía no hay materias registradas."
    )

    pausa()


def buscar_materia_menu():
    imprimir_titulo("BUSCAR MATERIA")

    termino = input("Nombre o código de la materia: ")

    mostrar_lista(
        buscar_materias(termino),
        "No se encontraron materias."
    )

    pausa()


def ver_materia():
    imprimir_titulo("CONSULTAR MATERIA")

    id_materia = pedir_entero("ID de la materia: ")

    if id_materia is not None:
        materia = obtener_materia(id_materia)

        if materia is None:
            imprimir_error("Materia no encontrada.")
        else:
            mostrar_detalle(materia)

    pausa()


def actualizar_materia_menu():
    imprimir_titulo("ACTUALIZAR MATERIA")

    id_materia = pedir_entero("ID de la materia: ")

    if id_materia is None:
        return pausa()

    materia = obtener_materia(id_materia)

    if materia is None:
        imprimir_error("Materia no encontrada.")
        return pausa()

    imprimir_info(f"Editando: {materia.etiqueta()}")
    print("Deje vacío un campo si no desea cambiarlo.\n")

    cambios = {}

    for campo in ("nombre", "codigo", "creditos", "cupos"):
        actual = getattr(materia, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()

        if nuevo:
            cambios[campo] = nuevo

    if cambios:
        mostrar_resultado(
            *actualizar_materia(id_materia, cambios)
        )
    else:
        imprimir_info("No se realizaron cambios.")

    pausa()


def eliminar_materia_menu():
    imprimir_titulo("ELIMINAR MATERIA")

    id_materia = pedir_entero("ID de la materia: ")

    if id_materia is None:
        return pausa()

    materia = obtener_materia(id_materia)

    if materia is None:
        imprimir_error("Materia no encontrada.")
        return pausa()

    imprimir_info(f"Se eliminará: {materia.etiqueta()}")

    if confirmar("¿Confirma la eliminación?"):
        mostrar_resultado(eliminar_materia(id_materia))
    else:
        imprimir_info("Operación cancelada.")

    pausa()


def ver_materias_sin_cupo():
    imprimir_titulo("MATERIAS SIN CUPO")

    mostrar_lista(
        materias_sin_cupo(),
        "Todas las materias tienen cupos disponibles."
    )

    pausa()


# =====================================================================
# MENÚ DE MATRÍCULAS
# =====================================================================

def registrar_matricula():
    imprimir_titulo("REGISTRAR MATRÍCULA")

    imprimir_info("Estudiantes registrados:")
    mostrar_lista(obtener_estudiantes())

    imprimir_info("Materias registradas:")
    mostrar_lista(obtener_materias())

    datos = {
        "estudiante_id": pedir_entero("ID del estudiante: "),
        "materia_id": pedir_entero("ID de la materia: "),
        "periodo": input("Periodo académico: ").strip()
    }

    if datos["estudiante_id"] is None or datos["materia_id"] is None:
        imprimir_error("Los IDs deben ser números enteros.")
        return pausa()

    mostrar_resultado(*crear_matricula(datos))
    pausa()


def listar_matriculas():
    imprimir_titulo("MATRÍCULAS")

    mostrar_lista(
        obtener_matriculas(),
        "Todavía no hay matrículas registradas."
    )

    pausa()


def registrar_nota_menu():
    imprimir_titulo("REGISTRAR NOTA")

    mostrar_lista(obtener_matriculas())

    id_matricula = pedir_entero("ID de la matrícula: ")

    if id_matricula is None:
        return pausa()

    nota = input("Nota obtenida (0 a 20): ")

    mostrar_resultado(registrar_nota(id_matricula, nota))
    pausa()


def ver_certificado():
    imprimir_titulo("CERTIFICADO ACADÉMICO")

    id_matricula = pedir_entero("ID de la matrícula: ")

    if id_matricula is not None:
        texto = certificado(id_matricula)

        if texto is None:
            imprimir_error("No se encontró la matrícula.")
        else:
            print(texto)

    pausa()


def retirar_matricula_menu():
    imprimir_titulo("RETIRAR MATRÍCULA")

    id_matricula = pedir_entero("ID de la matrícula: ")

    if id_matricula is None:
        return pausa()

    matricula = obtener_matricula(id_matricula)

    if matricula is None:
        imprimir_error("Matrícula no encontrada.")
        return pausa()

    imprimir_info(f"Se retirará: {matricula.etiqueta()}")

    if confirmar("¿Confirma el retiro de la matrícula?"):
        mostrar_resultado(retirar_matricula(id_matricula))
    else:
        imprimir_info("Operación cancelada.")

    pausa()


# =====================================================================
# RESUMEN ACADÉMICO
# =====================================================================

def resumen():
    imprimir_titulo("RESUMEN ACADÉMICO")

    estudiantes = obtener_estudiantes()
    materias = obtener_materias()
    matriculas = obtener_matriculas()

    carreras = set()

    for estudiante in estudiantes:
        carreras.add(estudiante.carrera)

    aprobadas = 0

    for matricula in matriculas:
        if matricula.esta_aprobada():
            aprobadas += 1

    sin_cupo = materias_sin_cupo()

    print(f"  Estudiantes       : {len(estudiantes)}")
    print(f"  Carreras          : {len(carreras)}")
    print(f"  Materias          : {len(materias)}")
    print(f"  Matrículas        : {len(matriculas)}")
    print(f"  Matrículas aprobadas: {aprobadas}")
    print(f"  Materias sin cupo : {len(sin_cupo)}")

    id_estudiante = pedir_entero(
        "\nID del estudiante para consultar su promedio "
        "(0 para omitir): "
    )

    if id_estudiante is not None and id_estudiante > 0:
        promedio = promedio_de_estudiante(id_estudiante)

        if promedio is None:
            imprimir_info("El estudiante no tiene matrículas.")
        else:
            print(f"  Promedio del estudiante: {promedio:.2f}/20")

    pausa()


# =====================================================================
# MENÚS: DICCIONARIOS TECLA -> (TEXTO, FUNCIÓN)
# =====================================================================

MENU_ESTUDIANTES = {
    "1": ("Registrar estudiante", crear_estudiante_menu),
    "2": ("Ver todos", listar_estudiantes),
    "3": ("Buscar", buscar_estudiante_menu),
    "4": ("Ver por ID", ver_estudiante),
    "5": ("Actualizar", actualizar_estudiante_menu),
    "6": ("Eliminar", eliminar_estudiante_menu),
    "0": ("Volver", None),
}

MENU_MATERIAS = {
    "1": ("Registrar materia", crear_materia_menu),
    "2": ("Ver todas", listar_materias),
    "3": ("Buscar", buscar_materia_menu),
    "4": ("Ver por ID", ver_materia),
    "5": ("Actualizar", actualizar_materia_menu),
    "6": ("Eliminar", eliminar_materia_menu),
    "7": ("Ver materias sin cupo", ver_materias_sin_cupo),
    "0": ("Volver", None),
}

MENU_MATRICULAS = {
    "1": ("Registrar matrícula", registrar_matricula),
    "2": ("Ver todas", listar_matriculas),
    "3": ("Registrar nota", registrar_nota_menu),
    "4": ("Ver certificado", ver_certificado),
    "5": ("Retirar matrícula", retirar_matricula_menu),
    "0": ("Volver", None),
}


def ejecutar_menu(titulo, opciones):
    while True:
        imprimir_titulo(titulo)

        for tecla, (texto, funcion) in opciones.items():
            print(f"  {tecla}. {texto}")

        print()
        tecla = input("Opción: ").strip()

        if tecla not in opciones:
            imprimir_error("Opción no válida.")
            pausa()
            continue

        texto, funcion = opciones[tecla]

        if funcion is None:
            break

        funcion()


# =====================================================================
# MENÚ PRINCIPAL
# =====================================================================

def main():
    while True:
        imprimir_titulo("SISTEMA DE GESTIÓN ACADÉMICA")

        print("  1. Estudiantes")
        print("  2. Materias")
        print("  3. Matrículas")
        print("  4. Resumen académico")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()

        if tecla == "1":
            ejecutar_menu("GESTIÓN DE ESTUDIANTES", MENU_ESTUDIANTES)

        elif tecla == "2":
            ejecutar_menu("GESTIÓN DE MATERIAS", MENU_MATERIAS)

        elif tecla == "3":
            ejecutar_menu("GESTIÓN DE MATRÍCULAS", MENU_MATRICULAS)

        elif tecla == "4":
            resumen()

        elif tecla == "0":
            imprimir_info("¡Hasta luego!")
            break

        else:
            imprimir_error("Opción no válida.")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
