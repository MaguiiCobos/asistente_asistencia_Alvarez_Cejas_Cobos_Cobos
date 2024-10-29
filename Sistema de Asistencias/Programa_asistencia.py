import cv2
import face_recognition as fr
import os
import numpy
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox

# Crear la ventana principal de tkinter (aunque no se mostrará)
root = tk.Tk()
root.withdraw()  # Oculta la ventana principal


# Crear base de datos
ruta = 'Inscriptos'
mis_imagenes = []
nombres_empleados = []
lista_empleados = os.listdir(ruta)

for nombre in lista_empleados:

    imagen_actual = cv2.imread(f"{ruta}/{nombre}")
    mis_imagenes.append(imagen_actual)
    nombres_empleados.append(os.path.splitext(nombre)[0])


print(nombres_empleados)

# Codificar imagenes
def codificar(imagenes):

    # Crear una lista nueva
    lista_codificada = []

    # Pasar todas las imagenes a RGB
    for imagen in imagenes:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

        # Codificar
        codificado = fr.face_encodings(imagen)[0]

        # Agregar a la lista
        lista_codificada.append(codificado)

    # Devolver lista codificada
    return lista_codificada

# Registrar los ingresos
def registrar_ingresos(persona):
    f = open("registro.csv", "r+")
    lista_datos = f.readlines()
    nombres_registro = []

    for linea in lista_datos:
        ingreso = linea.split(',')
        nombres_registro.append(ingreso[0])

    if persona not in nombres_registro:
        ahora = datetime.now()
        str_ahora = ahora.strftime('%H:%M:%S')
        f.writelines(f"\n{persona}, {str_ahora}")


#funcion agregada
def entregar_cronograma():
    f = open("cronograma.csv", "r+")
    lista_datos = f.readlines()
    print(lista_datos[1:])

def registro(imagen):
    nombre_inscripto = input("Ingrese su nombre y apellido: ")
    ruta = f"Inscriptos/{nombre_inscripto}.jpg"
    cv2.imwrite(ruta, imagen)
    print("Te has registrado con exito")

def validar_imagenes():
    # Tomar una imagen de camara web
    captura = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # Leer imagen de la camara
    exito, imagen = captura.read()
    if not exito:
        print("No se ha podido tomar la captura")
    else:

        # Reconocer cara en captura
        cara_captura = fr.face_locations(imagen)

        # Codificar cara capturada
        cara_captura_codificada = fr.face_encodings(imagen, cara_captura)

        # Buscar coincidencias | Doble loop
        for cara_codif, cara_ubic in zip(cara_captura_codificada, cara_captura):
            coincidencias = fr.compare_faces(lista_empleados_codificada, cara_codif)
            distancias = fr.face_distance(lista_empleados_codificada, cara_codif)

            print(distancias)

            indice_coincidencia = numpy.argmin(distancias)

            # Mostrar si existen coincidencias
            if distancias[indice_coincidencia] > 0.6:
                opcion = simpledialog.askstring("Inscribirse", "No estas en la lista de inscriptos\nDeseas registarte? (S/N): ")
                if opcion:
                    opcion = opcion.strip().upper()
                    if opcion == "S":
                        registro(imagen)
                    else:
                        print("Nos vimos")
            else:

                # Buscar el nombre del empleado encontrado
                nombre = nombres_empleados[indice_coincidencia]
                print(f"Bienvenid@, {nombre}, puedes ingresar a la reunion")

                #Agregamos funcion para dar el cronograma de la reunion
                entregar_cronograma()

                y1, x2, y2, x1 = cara_ubic

                cv2.rectangle(imagen, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(imagen, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(imagen, nombre, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                registrar_ingresos(nombre)

                # Mostrar la imagen obtenida
                cv2.imshow("Imagen web", imagen)

                # Mantener ventana abierta
                #cv2.waitKey(0)


lista_empleados_codificada = codificar(mis_imagenes)

# Mensaje de bienvenida
messagebox.showinfo("Registro de Asistencia", "Bienvenid@ al sistema de registro de asistencia de Invictus")
# Solicitar al usuario si desea registrarse
opcion = simpledialog.askstring("Registro", "¿Quieres registrarte? (S/N):")

if opcion:
    opcion = opcion.strip().upper()
    if opcion == "S":
        print("Validaremos tu imagen para saber si estas registrado")
        validar_imagenes()
        
    elif opcion == "N":
        print("Has elegido no registrarte.")
    else:
        print("Opcion no valida. Por favor, elige 'S' o 'N'.")
else:
    messagebox.showwarning("Advertencia", "No se ha ingresado ninguna opción.")