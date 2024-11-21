from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistroForm
from django.urls import reverse
from .models import Historial
from django.contrib.auth.hashers import make_password,check_password
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .utils import preprocess_image, run_inference
from .utils import preprocess_image, predict_image
from .utils import run_inference 
from .models import Paciente, Deteccion, Usuario, Rol  # Asegúrate de incluir todos los modelos necesarios
from .forms import HistorialForm
import base64
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import Deteccion, Paciente
from django.db import IntegrityError
from datetime import datetime, timedelta



# Vista base - renderiza la página de inicio
def inicioviews(request):
    if request.session.get('usuario_id'):
        usuario = Usuario.objects.get(id=request.session.get('usuario_id'))
        print("Usuario:", usuario.user)
        return render(request, 'inicio.html', {'usuario': usuario})
    return render(request, 'inicio.html')

# Vista para mostrar la página de inicio de sesión
def loginviews(request):
    return render(request, "login.html") 




def login_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        contraseña = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(email=email)

            # Verificar la contraseña
            if check_password(contraseña, usuario.contraseña):
                request.session['usuario_id'] = usuario.id
                messages.success(request, f"Bienvenido, {usuario.nombre_completo}!")
                return redirect('inicio')
            else:
                messages.error(request, "Correo o contraseña incorrectos.")
        except Usuario.DoesNotExist:
            messages.error(request, "Correo o contraseña incorrectos.")
    return render(request, 'login.html')


def registrar_usuario(request):
    if request.method == 'POST':
        nombre_completo = request.POST.get('nombre_completo')
        email = request.POST.get('email')
        user = request.POST.get('user')
        contraseña = request.POST.get('password')

        # Validar si el correo ya está registrado
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está en uso.")
            return redirect('login')

        # Asignar rol por defecto
        rol_invitado, created = Rol.objects.get_or_create(nombre='invitado')

        # Crear y guardar el usuario
        usuario = Usuario.objects.create(
            nombre_completo=nombre_completo,
            email=email,
            user=user,
            contraseña=make_password(contraseña),  # Hash de la contraseña
            rol=rol_invitado
        )
        usuario.save()
        messages.success(request, "Te has registrado correctamente. Ahora puedes iniciar sesión.")
        return redirect('login')
    return render(request, "login.html")


#def login(request):
#    return render(request, 'login.html')

def inicio(request):
    return render(request, 'inicio.html')

def escaneo(request):
    return render(request, 'escaneo.html')

def resultado(request):
    return render(request, 'resultado.html')

#def historial(request):
#    return render(request, 'historial.html')
 
def historial(request):
    dni = request.GET.get('dni', '').strip()  # Obtener el DNI ingresado y eliminar espacios

    # Validación del DNI
    if dni:
        if not dni.isdigit() or len(dni) != 8:  # Verificar que sea numérico y tenga 8 dígitos
            messages.error(request, "Por favor, ingrese un DNI válido de 8 dígitos.")
            return render(request, 'historial.html', {'historiales': []})  # No mostrar resultados

        # Buscar registros por DNI
        historiales = Historial.objects.filter(dni_paciente=dni)
        if not historiales.exists():
            messages.warning(request, f"No se encontraron resultados para el DNI {dni}.")
    else:
        messages.error(request, "Por favor, ingrese un DNI válido para buscar.")
        historiales = []  # No mostrar resultados si el campo está vacío

    return render(request, 'historial.html', {'historiales': historiales})

def load_tflite_interpreter():
    current_directory = os.path.dirname(__file__)
    model_path = os.path.join(current_directory, 'ml_models', 'modelo1.tflite')
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

interpreter = load_tflite_interpreter()

from django.utils import timezone  # Asegúrate de importar esto si decides establecer la fecha manualmente

def guardar_resultado(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dni = data.get('dni')
            imagen_base64 = data.get('imagen')
            resultado = data.get('resultado')
            precision = data.get('precision')

            if not dni or not imagen_base64 or not resultado or not precision:
                return JsonResponse({'error': 'Faltan datos en la solicitud'}, status=400)

            # Crea la detección, y `fecha` se registrará automáticamente con la fecha actual
            Deteccion.objects.create(
                dni_paciente=dni,
                imagen=imagen_base64,
                resultado=resultado,
                precision=precision,
                # Si quieres especificar manualmente, usa: fecha=timezone.now()
            )

            return JsonResponse({'success': 'Detección registrada exitosamente'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato de JSON inválido'}, status=400)
        except Exception as e:
            print("Error al procesar la solicitud:", e)
            return JsonResponse({'error': 'Error al registrar la detección.'}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)




def procesar_imagen(request):
    if request.method == 'POST' and request.FILES.get('imagen'):
        image_file = request.FILES['imagen']
        image_path = default_storage.save('tmp/' + image_file.name, ContentFile(image_file.read()))

        # Ejecutar la inferencia en la imagen
        output_data = run_inference(default_storage.path(image_path))
        predicted_class = np.argmax(output_data[0])
        probability = np.max(output_data[0]) * 100

        # Mapeo de la predicción a las etiquetas
        result_map = {
            0: "Maligno",
            1: "Benigno",
            2: "Desconocida"
        }
        result = result_map.get(predicted_class, "Resultado no válido")

        # Preparar respuesta en JSON
        response_data = {
            'prediction': result,
            'probability': round(probability, 2)
        }
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Método no permitido o archivo no recibido'}, status=400)



def buscar_paciente(request):
    dni = request.GET.get('dni')
    try:
        paciente = Paciente.objects.get(dni=dni)
        return JsonResponse({
            'existe': True,
            'nombres': paciente.nombres,
            'apellidos': paciente.apellidos,
            'fecha_nacimiento': paciente.fecha_nacimiento.strftime('%Y-%m-%d')
        })
    except Paciente.DoesNotExist:
        return JsonResponse({'existe': False})




def guardar_historial(request):
    if request.method == "POST":
        form = HistorialForm(request.POST, request.FILES)
        if form.is_valid():
            historial = form.save(commit=False)
            # Leer la imagen del formulario y convertirla a base64
            imagen = request.FILES["imagen"]
            imagen_base64 = base64.b64encode(imagen.read()).decode("utf-8")
            historial.imagen_base64 = imagen_base64  # Asignar el base64 al campo del modelo
            historial.save()
            return redirect('historial_success')  # Redirigir a una página de éxito
    else:
        form = HistorialForm()
    return render(request, "guardar_historial.html", {"form": form})


from django.shortcuts import render, get_object_or_404
from .models import Deteccion, Paciente

def historial(request):
    dni = request.GET.get('dni')
    user_id = request.GET.get('user_id')

    # Filtrar registros de detección de acuerdo con los filtros proporcionados
    if dni and user_id:
        historiales = Deteccion.objects.filter(dni_paciente=dni, usuario_id=user_id)
    elif dni:
        historiales = Deteccion.objects.filter(dni_paciente=dni)
    elif user_id:
        historiales = Deteccion.objects.filter(usuario_id=user_id)
    else:
        historiales = Deteccion.objects.all()

    # Añadir nombres y apellidos de cada paciente si existe en la tabla de pacientes
    for historial in historiales:
        if historial.dni_paciente:  # Verificar si hay un dni_paciente presente
            try:
                paciente = Paciente.objects.get(dni=historial.dni_paciente)
                historial.nombres = paciente.nombres
                historial.apellidos = f"{paciente.apellido_paterno} {paciente.apellido_materno}"
            except Paciente.DoesNotExist:
                historial.nombres = "-"
                historial.apellidos = "-"
        else:
            historial.nombres = "-"
            historial.apellidos = "-"

    return render(request, 'historial.html', {'historiales': historiales})
def registrar_paciente(request):
    if request.method == 'POST':
        dni = request.POST.get('dni')
        nombres = request.POST.get('nombres')
        apellido_paterno = request.POST.get('apellido_paterno')
        apellido_materno = request.POST.get('apellido_materno')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        direccion = request.POST.get('direccion')
        numero_contacto = request.POST.get('numero_contacto')
        usuario_id = request.POST.get('usuario_id')

       # Validación de fecha de nacimiento
        try:
            fecha_nacimiento_obj = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            today = datetime.today().date()
            min_date = today - timedelta(days=365*150)  # Hace 150 años
            max_date = today  # Hoy

            if not (min_date <= fecha_nacimiento_obj <= max_date):
                messages.warning(request, "La fecha de nacimiento debe estar entre hace 150 años.")
                return render(request, 'escaneo.html')  # Permanecer en la misma página
        except (ValueError, TypeError):
            messages.warning(request, "Fecha de nacimiento inválida. Por favor, ingrese una fecha válida.")
            return render(request, 'escaneo.html')  # Permanecer en la misma página

        # Obtener el usuario si se proporcionó un ID válido
        usuario = None
        if usuario_id:
            try:
                usuario = Usuario.objects.get(id=usuario_id)
            except Usuario.DoesNotExist:
                messages.warning(request, "Usuario no encontrado, se guardará sin usuario asignado.")
                usuario = None
        try:
            # Intentar crear un nuevo paciente
            Paciente.objects.create(
                dni=dni,
                nombres=nombres,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                fecha_nacimiento=fecha_nacimiento,
                direccion=direccion,
                numero_contacto=numero_contacto,
                usuario=usuario,
            )
            messages.success(request, "Paciente registrado exitosamente.")
        except IntegrityError:
            # Capturar error de clave única y mostrar un mensaje
            messages.warning(request, "El paciente con este DNI ya existe. Por favor, verifique los datos.")

        # Renderizar la misma página con los mensajes
        return render(request, 'escaneo.html')

    return render(request, 'escaneo.html')



def buscar_paciente(request):
    dni = request.GET.get('dni')
    try:
        paciente = Paciente.objects.get(dni=dni)
        return JsonResponse({
            'existe': True,
            'nombres': paciente.nombres,
            'apellido_paterno': paciente.apellido_paterno,
            'apellido_materno': paciente.apellido_materno,
        })
    except Paciente.DoesNotExist:
        return JsonResponse({'existe': False})



def eliminar_historial(request, id):
    historial = get_object_or_404(Deteccion, id=id)
    
    if request.method == 'POST':
        historial.delete()
        messages.success(request, 'El historial ha sido eliminado exitosamente.')
        return redirect('historial')  # Redirige al historial después de eliminar

    return render(request, 'confirmar_eliminar.html', {'historial': historial})
