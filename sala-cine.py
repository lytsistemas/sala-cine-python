class Asiento:
    def __init__(self, numero, fila, precio_base):
        # Inicializa el asiento con número, fila y el precio base
        self.__numero = numero
        self.__fila = fila
        self.__reservado = False
        self.__precio_base = precio_base

    def reservar(self, precio):
        # Reserva el asiento, asignando el precio correspondiente
        if self.__reservado:
            raise ValueError(f"El asiento {self.__numero} ya está reservado.")
        self.__reservado = True
        self.__precio = precio

    def cancelar_reserva(self):
        # Cancela la reserva del asiento
        if not self.__reservado:
            raise ValueError(f"El asiento {self.__numero} no está reservado.")
        self.__reservado = False
        self.__precio = None

    def obtener_precio(self):
        # Devuelve el precio del asiento, si está reservado aplica el precio con descuento
        return self.__precio_base if not self.__reservado else self.__precio

    def mostrar_asiento(self):
        # Devuelve una cadena con el estado del asiento y su precio
        estado = "Reservado" if self.__reservado else "Disponible"
        precio = self.obtener_precio()
        return f"Asiento {self.__numero}, Fila {self.__fila} - {estado} - Precio: {precio}€"

    def obtener_numero(self):
        # Obtiene el número del asiento
        return self.__numero

    def obtener_fila(self):
        # Obtiene la fila del asiento
        return self.__fila

    def esta_reservado(self):
        # Retorna si el asiento está reservado
        return self.__reservado


class SalaCine:
    def __init__(self, precio_base):
        # Inicializa la sala de cine con una lista vacía de asientos y un precio base
        self.__asientos = []
        self.__precio_base = precio_base


    def agregar_asiento(self, numero, fila):
        # Comprobar si ya existe un asiento con el mismo número y fila
        for asiento in self.__asientos:
            if asiento.obtener_numero() == numero and asiento.obtener_fila() == fila:
                raise ValueError(f"Ya existe un asiento con número {numero} en la fila {fila}.")
        # Si no se encontró ningún asiento duplicado, añadir el nuevo asiento
        nuevo_asiento = Asiento(numero, fila, self.__precio_base)
        self.__asientos.append(nuevo_asiento)


    def reservar_asiento(self, numero, fila, dia, edad):
        # Busca el asiento en la sala
        asiento = self.buscar_asiento(numero, fila)
        
        # Verifica si el asiento ya está reservado
        if asiento.esta_reservado():
            raise ValueError(f"El asiento {numero} en la fila {fila} ya está reservado. No se puede realizar la reserva.")
        
        # Calcular el precio con los descuentos
        precio = self.__precio_base

        #
        if self.es_dia_especial(dia) and self.es_edad_reducida(edad):
            precio *= 0.5  # 50% de descuento

        else:

            # Descuento por día del espectador (miércoles)
            if self.es_dia_especial(dia):
                precio *= 0.8  # 20% de descuento

            # Descuento por edad (mayores de 65 años)
            if self.es_edad_reducida(edad):
                precio *= 0.7  # 30% de descuento

        # Reserva el asiento con el precio calculado
        asiento.reservar(precio)

    def cancelar_reserva(self, numero, fila):
        # Cancela la reserva de un asiento
        asiento = self.buscar_asiento(numero, fila)
        asiento.cancelar_reserva()

    def mostrar_asientos(self):
        # Muestra todos los asientos de la sala con su estado y precio
        if not self.__asientos:
            print("No hay asientos disponibles en la sala.")
            return
        for asiento in self.__asientos:
            print(asiento.mostrar_asiento())

    def buscar_asiento(self, numero, fila):
        # Busca un asiento por su número y fila
        for asiento in self.__asientos:
            if asiento.obtener_numero() == numero and asiento.obtener_fila() == fila:
                return asiento
        raise ValueError(f"No se encontró el asiento {numero} en la fila {fila}.")

    def es_numero_positivo(self, valor):
        # Función genérica para validar si un valor es un número entero positivo
        return isinstance(valor, int) and valor > 0

    def es_dia_valido(self, dia):
        # Valida que el día esté en la lista de días válidos
        dias_validos = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        return dia in dias_validos

    def es_dia_especial(self, dia):
        # Función para comprobar si el día es miércoles (día con descuento)
        dias_especiales = ["miércoles"]
        return dia in dias_especiales

    def es_edad_reducida(self, edad):
        # Función para comprobar si la edad es mayor a 65 (descuento por edad)
        return edad > 65

    def es_edad_valida(self, edad):
        # Función para comprobar si la edad es válida
        return edad > 0


def mostrar_menu():
    # Muestra el menú principal con las opciones disponibles
    print("\n--- Menú de Gestión de Sala de Cine, IBM SkillsBuild ---")
    print("1. Agregar asiento")
    print("2. Reservar asiento")
    print("3. Cancelar reserva")
    print("4. Mostrar todos los asientos")
    print("5. Buscar asiento")
    print("6. Salir")


def obtener_entrada_valida(prompt, tipo_entrada, validacion_func, mensaje_error):
    # Función para obtener una entrada válida de usuario
    while True:
        entrada = input(prompt)
        
        if tipo_entrada == 'numero':  # Esperamos un número
            if entrada.isdigit() and validacion_func(int(entrada)):
                return int(entrada)
            else:
                print(mensaje_error)
        
        elif tipo_entrada == 'cadena':  # Esperamos un día de lunes a domingo
            if entrada.strip() and validacion_func(entrada.lower()):  
                return entrada.lower()
            else:
                print(mensaje_error)
        
        else:
            print("Tipo de entrada no soportado.")
            break


def ejecutar():
    # Crear una sala de cine con un precio base de 10 euros
    sala = SalaCine(10)

    while True:
        # Mostrar el menú de opciones
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            # Agregar un asiento a la sala
            numero = obtener_entrada_valida("Introduce el número del asiento: ", 'numero', 
                                            sala.es_numero_positivo, "Error: El número de asiento debe ser un número entero positivo.")

            fila = obtener_entrada_valida("Introduce la fila del asiento: ", 'numero', 
                                            sala.es_numero_positivo, "Error: La fila debe ser un número entero positivo.")

            try:
                sala.agregar_asiento(numero, fila)
                print(f"Asiento {numero} en la fila {fila} agregado exitosamente.")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "2":
            # Reservar un asiento
            numero = obtener_entrada_valida("Introduce el número del asiento: ", 'numero', 
                                            sala.es_numero_positivo, "Error: El número de asiento debe ser un número entero positivo.")

            fila = obtener_entrada_valida("Introduce la fila del asiento: ", 'numero', 
                                            sala.es_numero_positivo, "Error: La fila debe ser un número entero positivo.")

            try:
                # Verificar si el asiento ya está reservado antes de pedir más datos
                asiento = sala.buscar_asiento(numero, fila)
                if asiento.esta_reservado():
                    print(f"Error: El asiento {numero} en la fila {fila} ya está reservado.")
                    continue
                
                #Comprobar que el día es correcto
                dia = obtener_entrada_valida("Introduce el día de la semana (ej. miércoles):", 'cadena', sala.es_dia_valido, 
                                            "Error: El día debe ser uno de los siguientes: lunes, martes, miércoles, jueves, viernes, sábado, domingo.")

                #Comprobar que la edad es correcta
                edad = obtener_entrada_valida("Introduce la edad del espectador: ", 'numero', sala.es_numero_positivo, 
                                             "Error: La edad debe ser un número entero positivo.")

                sala.reservar_asiento(numero, fila, dia, edad)
                print(f"Asiento {numero} en la fila {fila} reservado exitosamente.")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "3":
            # Cancelar una reserva
            numero = obtener_entrada_valida("Introduce el número del asiento: ", 'numero', 
                                            sala.es_numero_positivo, "Error: El número de asiento debe ser un número entero positivo.")

            fila = obtener_entrada_valida("Introduce la fila del asiento: ", 'numero', 
                                            sala.es_numero_positivo, "Error: La fila debe ser un número entero positivo.")

            try:
                sala.cancelar_reserva(numero, fila)
                print(f"Reserva del asiento {numero} en la fila {fila} cancelada exitosamente.")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "4":
            # Mostrar todos los asientos
            sala.mostrar_asientos()

        elif opcion == "5":
            # Buscar un asiento
            numero = obtener_entrada_valida("Introduce el número del asiento: ", 'numero', 
                                            sala.es_numero_positivo, "Error: El número de asiento debe ser un número entero positivo.")

            fila = obtener_entrada_valida("Introduce la fila del asiento: ", 'numero', 
                                            sala.es_numero_positivo, "Error: La fila debe ser un número entero positivo.")
            try:            
                asiento = sala.buscar_asiento(numero, fila)
                print (asiento.mostrar_asiento())
            except ValueError as e:
                print(f"Error: {e}")


        elif opcion == "6":
            # Salir del programa
            print("¡Gracias por usar el sistema de reservas del cine! Hasta pronto!")
            break

        else:
            # Si el usuario ingresa una opción inválida
            print("Opción no válida. Por favor, selecciona una opción del 1 al 5.")


# Ejecutar el programa
ejecutar()

