from datetime import date


# =====================================================================
# CLASE BASE: lo que los tres modelos comparten
# =====================================================================
class ModeloBase:
    """Padre de todos los modelos. Guarda el id y define el comportamiento común."""

    def __init__(self, id_registro):
        self.id = int(id_registro)

    # ---- ÚNICO MÉTODO DE CLASE DEL PROYECTO ----
    @classmethod
    def desde_diccionario(cls, datos):
        """Diccionario -> objeto. Escrito UNA vez y usado por los tres modelos.
        cls es la clase que llamó: Cliente, Producto o Venta."""
        datos = dict(datos)                 # copia, para no tocar el original
        id_registro = datos.pop("id")       # saco el id
        return cls(id_registro, **datos)    # el resto son los campos del modelo

    # ---- MÉTODOS DE INSTANCIA ----
    def a_diccionario(self):
        # Objeto -> diccionario. Cada hijo agrega sus campos.
        return {"id": self.id}

    def etiqueta(self):
        # POLIMORFISMO: cada hijo la reescribe a su manera
        return f"registro {self.id}"

    def __str__(self):
        # Lo que se ve al hacer print(objeto). Llama a etiqueta(),
        # así que cada modelo se imprime distinto sin cambiar esta línea.
        return f"[{self.id}] {self.etiqueta()}"


# =====================================================================
# HERENCIA: Persona es la base de Cliente (y mañana, de Estudiante)
# =====================================================================
class Persona(ModeloBase):
    """Todo lo que tiene una persona del sistema."""

    def __init__(self, id_registro, nombre, apellido, email):
        super().__init__(id_registro)      # el padre guarda el id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}{self.carnet}{self.carrera}"

    def a_diccionario(self):
        datos = super().a_diccionario()    # {"id": ...} que arma el padre
        datos["nombre"] = self.nombre
        datos["apellido"] = self.apellido
        datos["email"] = self.email
        datos["carnet"] = self.carnet
        datos["carrera"] = self.carrera
        return datos

    def etiqueta(self):
        return self.nombre_completo()


class Estudiante(Persona):
    """Cliente ES UNA Persona, con teléfono y ciudad."""

    def __init__(self, id_registro, nombre, apellido, email, carnet="", carrera=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.carnet = carnet
        self.carrera = carrera

    def a_diccionario(self):
        datos = super().a_diccionario()    # reutiliza lo de Persona
        datos["carnet"] = self.carnet
        datos["carrera"] = self.carrera
        return datos

    def etiqueta(self):
        # Sobrescribe y EXTIENDE la del padre
        return f"{super().etiqueta()} · {self.nombre} · {self.apellido}, {self.carnet}, {self.carrera}"


# =====================================================================
# ÚNICA CLASE CON ATRIBUTOS Y MÉTODOS ESTÁTICOS
# =====================================================================
class Materia(ModeloBase):
    """Producto ES UN ModeloBase. Aquí viven los ejemplos de lo estático."""

    # ATRIBUTOS ESTÁTICOS (de clase): existen una sola vez, no por objeto
    CUPOS_MAXIMOS = 30          # regla del negocio, igual para todos los productos
    NOTA_APROBACION = 14                # 15 %
    total_creados = 0         # contador compartido

    def __init__(self, id_registro, nombre, codigo, creditos, cupos=CUPOS_MAXIMOS):
        super().__init__(id_registro)
        self.nombre = nombre
        self.codigo = float(codigo)
        self.creditos = int(creditos)
        self.cupos = int(cupos)
        Materia.total_creados += 1        # se modifica en la CLASE, no en self

    # MÉTODOS ESTÁTICOS: reglas que no necesitan ningún producto concreto
    @staticmethod
    def es_nota_valida(valor):
        try:
            return 0<= float(valor) <=20
        except (TypeError, ValueError):
            return False



    def hay_cupo(self, cantidad):
        return 0 < cantidad <= self.cupos

    def ocupar_cupo(self, cantidad):
        if self.hay_cupo(cantidad):
            self.cupos_disponibles -= cantidad
            return True
        return False

    def liberar_cupo(self, cantidad):
        self.cupos_disponibles += cantidad

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["codigo"] = self.precio
        datos["creditos"] = self.creditos
        datos["cupos_disponibles"] = self.cupos_disponibles
        return datos

    def etiqueta(self):
        alerta = " ⚠ stock bajo" if self.stock_bajo() else ""
        return f"{self.nombre} · ${self.codigo} ·{self.credito} credito {self.cupos} cupos"


# =====================================================================
class Matricula(ModeloBase):
    """Venta simple: un cliente, un producto, una cantidad."""

    def __init__(self, id_registro, estudiante_id, materia_id, periodo,
                 nota , fecha=""):
        super().__init__(id_registro)
        self.estudiante_id = int(estudiante_id)
        self.materia_id = (materia_id)
        self.periodo = int(periodo)
        self.nota = float(nota)
        self.fecha = fecha or date.today().isoformat()

    def calcular_total(self):
        # Se calcula cada vez; NO se guarda como atributo para que nunca
        # quede desactualizado si cambia la cantidad
        return round(self.cantidad * self.precio_unitario, 2)

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["estudiante_id"] = self.estudiante_id
        datos["materia_id"] = self.materia_id
        datos["periodo"] = self.periodo
        datos["nota"] = self.nota
        datos["fecha"] = self.fecha
        return datos

    def etiqueta(self):
        return (f"{self.fecha} · cliente {self.estudiante_id} · "
                f"{self.periodo} periodo {self.nota} "
        )