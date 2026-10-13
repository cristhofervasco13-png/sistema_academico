from abc import ABC, abstractmethod

from models import Estudiante, Materia, Matricula
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido


# Archivos donde se guardan los datos
gestor_estudiantes = GestorJSON("data/estudiantes.json")
gestor_materias = GestorJSON("data/materias.json")
gestor_matriculas = GestorJSON("data/matriculas.json")


# FUNCIONES GENERALES

def leer_objetos(gestor, modelo):
    datos = gestor.leer()
    objetos = []

    for dato in datos:
        objetos.append(modelo.desde_diccionario(dato))

    return objetos


def obtener_por_id(gestor, modelo, id):
    for objeto in leer_objetos(gestor, modelo):
        if objeto.id == id:
            return objeto

    return None


def siguiente_id(gestor):
    datos = gestor.leer()
    mayor = 0

    for dato in datos:
        if dato["id"] > mayor:
            mayor = dato["id"]

    return mayor + 1


def guardar_nuevo(gestor, objeto):
    datos = gestor.leer()
    datos.append(objeto.a_diccionario())
    return gestor.guardar(datos)


def reemplazar(gestor, objeto):
    datos = gestor.leer()

    for i in range(len(datos)):
        if datos[i]["id"] == objeto.id:
            datos[i] = objeto.a_diccionario()
            return gestor.guardar(datos)

    return False


def eliminar(gestor, id):
    datos = gestor.leer()
    nuevos = []

    for dato in datos:
        if dato["id"] != id:
            nuevos.append(dato)

    if len(datos) == len(nuevos):
        return False

    return gestor.guardar(nuevos)


def buscar(gestor, modelo, termino, campos):
    resultados = []
    termino = termino.lower().strip()

    for objeto in leer_objetos(gestor, modelo):
        for campo in campos:
            valor = str(getattr(objeto, campo)).lower()

            if termino in valor:
                resultados.append(objeto)
                break

    return resultados


def ids_registrados(gestor):
    ids = set()

    for dato in gestor.leer():
        ids.add(dato["id"])

    return ids


def indice_por_id(gestor, modelo):
    indice = {}

    for objeto in leer_objetos(gestor, modelo):
        indice[objeto.id] = objeto

    return indice


# FUNCIONES DE ESTUDIANTES

def carnets_registrados(excepto_id=None):
    carnets = set()

    for dato in gestor_estudiantes.leer():
        if dato["id"] != excepto_id:
            carnets.add(dato["carnet"].upper())

    return carnets


def emails_registrados(excepto_id=None):
    emails = set()

    for dato in gestor_estudiantes.leer():
        if dato["id"] != excepto_id:
            emails.add(dato["email"].lower())

    return emails


def validar_estudiante(datos, id_actual=None):
    nombre = datos.get("nombre", "").strip()
    apellido = datos.get("apellido", "").strip()
    email = datos.get("email", "").strip().lower()
    carnet = datos.get("carnet", "").strip().upper()
    carrera = datos.get("carrera", "").strip()

    if not nombre or not apellido or not email:
        return False, "El nombre, apellido y correo son obligatorios."

    if not carnet or not carrera:
        return False, "El carnet y la carrera son obligatorios."

    if not es_email_valido(email):
        return False, "El correo electrónico no es válido."

    if email in emails_registrados(id_actual):
        return False, "Ese correo ya está registrado."

    if carnet in carnets_registrados(id_actual):
        return False, "Ese carnet ya está registrado."

    return True, "Datos correctos."


def crear_estudiante(datos):
    valido, mensaje = validar_estudiante(datos)

    if not valido:
        return False, mensaje

    estudiante = Estudiante(
        siguiente_id(gestor_estudiantes),
        datos["nombre"].strip().title(),
        datos["apellido"].strip().title(),
        datos["email"].strip().lower(),
        datos["carnet"].strip().upper(),
        datos["carrera"].strip().title()
    )

    if guardar_nuevo(gestor_estudiantes, estudiante):
        return True, "Estudiante registrado correctamente."

    return False, "No se pudo guardar el estudiante."


def obtener_estudiantes():
    return leer_objetos(gestor_estudiantes, Estudiante)


def obtener_estudiante(id):
    return obtener_por_id(gestor_estudiantes, Estudiante, id)


def buscar_estudiantes(termino):
    return buscar(
        gestor_estudiantes,
        Estudiante,
        termino,
        ("nombre", "apellido", "email", "carnet", "carrera")
    )


def actualizar_estudiante(id, cambios):
    estudiante = obtener_estudiante(id)

    if estudiante is None:
        return False, "No existe ese estudiante."

    datos = estudiante.a_diccionario()

    for campo in cambios:
        if campo in datos and cambios[campo].strip():
            datos[campo] = cambios[campo].strip()

    valido, mensaje = validar_estudiante(datos, id)

    if not valido:
        return False, mensaje

    estudiante.nombre = datos["nombre"].title()
    estudiante.apellido = datos["apellido"].title()
    estudiante.email = datos["email"].lower()
    estudiante.carnet = datos["carnet"].upper()
    estudiante.carrera = datos["carrera"].title()

    if reemplazar(gestor_estudiantes, estudiante):
        return True, "Estudiante actualizado correctamente."

    return False, "No se pudo actualizar el estudiante."


def eliminar_estudiante(id):
    estudiante = obtener_estudiante(id)

    if estudiante is None:
        return False, "No existe ese estudiante."

    for matricula in leer_objetos(gestor_matriculas, Matricula):
        if matricula.estudiante_id == id:
            return False, "No se puede eliminar: tiene matrículas registradas."

    if eliminar(gestor_estudiantes, id):
        return True, "Estudiante eliminado correctamente."

    return False, "No se pudo eliminar el estudiante."


# FUNCIONES DE MATERIAS

def codigos_registrados(excepto_id=None):
    codigos = set()

    for dato in gestor_materias.leer():
        if dato["id"] != excepto_id:
            codigos.add(dato["codigo"].upper())

    return codigos


def validar_materia(datos, id_actual=None):
    nombre = datos.get("nombre", "").strip()
    codigo = datos.get("codigo", "").strip().upper()

    if not nombre or not codigo:
        return False, "El nombre y el código son obligatorios."

    if codigo in codigos_registrados(id_actual):
        return False, "Ese código de materia ya existe."

    try:
        creditos = int(datos["creditos"])
        cupos = int(datos["cupos"])
    except (ValueError, TypeError, KeyError):
        return False, "Los créditos y los cupos deben ser números enteros."

    if creditos < 1 or creditos > 10:
        return False, "Los créditos deben estar entre 1 y 10."

    if cupos < 0 or cupos > Materia.CUPOS_MAXIMOS:
        return False, "Los cupos deben estar entre 0 y 30."

    return True, "Datos correctos."


def crear_materia(datos):
    valido, mensaje = validar_materia(datos)

    if not valido:
        return False, mensaje

    materia = Materia(
        siguiente_id(gestor_materias),
        datos["nombre"].strip().title(),
        datos["codigo"].strip().upper(),
        int(datos["creditos"]),
        int(datos["cupos"])
    )

    if guardar_nuevo(gestor_materias, materia):
        return True, "Materia registrada correctamente."

    return False, "No se pudo guardar la materia."


def obtener_materias():
    return leer_objetos(gestor_materias, Materia)


def obtener_materia(id):
    return obtener_por_id(gestor_materias, Materia, id)


def buscar_materias(termino):
    return buscar(
        gestor_materias,
        Materia,
        termino,
        ("nombre", "codigo")
    )


def actualizar_materia(id, cambios):
    materia = obtener_materia(id)

    if materia is None:
        return False, "No existe esa materia."

    datos = materia.a_diccionario()

    for campo in cambios:
        if campo in datos and str(cambios[campo]).strip():
            datos[campo] = cambios[campo]

    valido, mensaje = validar_materia(datos, id)

    if not valido:
        return False, mensaje

    # No se permite reducir los cupos por debajo de las matrículas existentes.
    matriculados = 0

    for matricula in leer_objetos(gestor_matriculas, Matricula):
        if matricula.materia_id == id:
            matriculados += 1

    nuevos_cupos = int(datos["cupos"])

    if nuevos_cupos + matriculados > Materia.CUPOS_MAXIMOS:
        return False, "Los cupos exceden el máximo permitido."

    materia.nombre = str(datos["nombre"]).strip().title()
    materia.codigo = str(datos["codigo"]).strip().upper()
    materia.creditos = int(datos["creditos"])
    materia.cupos = nuevos_cupos

    if reemplazar(gestor_materias, materia):
        return True, "Materia actualizada correctamente."

    return False, "No se pudo actualizar la materia."


def eliminar_materia(id):
    materia = obtener_materia(id)

    if materia is None:
        return False, "No existe esa materia."

    for matricula in leer_objetos(gestor_matriculas, Matricula):
        if matricula.materia_id == id:
            return False, "No se puede eliminar: tiene matrículas registradas."

    if eliminar(gestor_materias, id):
        return True, "Materia eliminada correctamente."

    return False, "No se pudo eliminar la materia."


def materias_sin_cupo():
    resultado = []

    for materia in obtener_materias():
        if not materia.hay_cupo():
            resultado.append(materia)

    return resultado


# FUNCIONES DE MATRÍCULAS

def crear_matricula(datos):
    try:
        estudiante_id = int(datos["estudiante_id"])
        materia_id = int(datos["materia_id"])
    except (ValueError, TypeError, KeyError):
        return False, "Los IDs del estudiante y de la materia deben ser números."

    estudiante = obtener_estudiante(estudiante_id)
    materia = obtener_materia(materia_id)
    periodo = datos.get("periodo", "").strip()

    if estudiante is None:
        return False, "El estudiante no existe."

    if materia is None:
        return False, "La materia no existe."

    if not periodo:
        return False, "El periodo académico es obligatorio."

    if not materia.hay_cupo():
        return False, "La materia no tiene cupos disponibles."

    for matricula in leer_objetos(gestor_matriculas, Matricula):
        if (
            matricula.estudiante_id == estudiante_id
            and matricula.materia_id == materia_id
            and matricula.periodo.lower() == periodo.lower()
        ):
            return False, "El estudiante ya está matriculado en esa materia."

    matricula = Matricula(
        siguiente_id(gestor_matriculas),
        estudiante_id,
        materia_id,
        periodo
    )

    # Se descuenta un cupo y se guardan ambos cambios.
    materia.ocupar_cupo()

    if not reemplazar(gestor_materias, materia):
        return False, "No se pudo actualizar el cupo de la materia."

    if guardar_nuevo(gestor_matriculas, matricula):
        return True, "Matrícula registrada correctamente."

    materia.liberar_cupo()
    reemplazar(gestor_materias, materia)
    return False, "No se pudo guardar la matrícula."


def obtener_matriculas():
    return leer_objetos(gestor_matriculas, Matricula)


def obtener_matricula(id):
    return obtener_por_id(gestor_matriculas, Matricula, id)


def registrar_nota(id, nota):
    matricula = obtener_matricula(id)

    if matricula is None:
        return False, "No existe esa matrícula."

    if not Materia.es_nota_valida(nota):
        return False, "La nota debe estar entre 0 y 20."

    matricula.nota = float(nota)

    if reemplazar(gestor_matriculas, matricula):
        return True, "Nota registrada correctamente. Estado: " + matricula.estado()

    return False, "No se pudo registrar la nota."


def retirar_matricula(id):
    matricula = obtener_matricula(id)

    if matricula is None:
        return False, "No existe esa matrícula."

    materia = obtener_materia(matricula.materia_id)

    if materia is not None:
        materia.liberar_cupo()

        if not reemplazar(gestor_materias, materia):
            return False, "No se pudo actualizar el cupo."

    if eliminar(gestor_matriculas, id):
        return True, "Matrícula retirada correctamente."

    return False, "No se pudo retirar la matrícula."


def certificado(id):
    matricula = obtener_matricula(id)

    if matricula is None:
        return None

    estudiante = obtener_estudiante(matricula.estudiante_id)
    materia = obtener_materia(matricula.materia_id)

    if estudiante is None or materia is None:
        return None

    texto = (
        "\n--- CERTIFICADO ACADÉMICO ---\n"
        + "Estudiante: " + estudiante.nombre_completo() + "\n"
        + "Carnet: " + estudiante.carnet + "\n"
        + "Carrera: " + estudiante.carrera + "\n"
        + "Materia: " + materia.nombre + "\n"
        + "Código: " + materia.codigo + "\n"
        + "Periodo: " + matricula.periodo + "\n"
        + "Fecha: " + matricula.fecha + "\n"
        + "Nota: " + str(matricula.nota) + "\n"
        + "Estado: " + matricula.estado()
    )

    return texto


def matriculas_por_estudiante():
    # Diccionario de listas: cada estudiante tiene sus matrículas.
    resultado = {}

    for matricula in obtener_matriculas():
        if matricula.estudiante_id not in resultado:
            resultado[matricula.estudiante_id] = []

        resultado[matricula.estudiante_id].append(matricula)

    return resultado


def promedio_de_estudiante(id):
    suma = 0
    cantidad = 0

    for matricula in obtener_matriculas():
        if matricula.estudiante_id == id:
            suma += matricula.nota
            cantidad += 1

    if cantidad == 0:
        return None

    return suma / cantidad
