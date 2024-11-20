from django.db import models
from django.utils import timezone

# Modelo para Rol
class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# Modelo para Usuario
class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    user = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=255)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    fecharegistro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_completo} - {self.rol.nombre_completo}"

# Modelo para Paciente
class Paciente(models.Model): 
    id = models.BigAutoField(primary_key=True)
    dni = models.CharField(max_length=8, unique=True, null=True, blank=True)
    nombres = models.CharField(max_length=100, null=True, blank=True)
    apellido_paterno = models.CharField(max_length=100, null=True, blank=True)
    apellido_materno = models.CharField(max_length=100, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.TextField(blank=True, null=True)
    numero_contacto = models.CharField(max_length=15, blank=True, null=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'pacientes'

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno} ({self.dni})"

# Modelo para Detección
class Deteccion(models.Model):
    id = models.AutoField(primary_key=True)
    dni_paciente = models.BigIntegerField(null=True, blank=True)  # Almacena el DNI directamente
    imagen = models.TextField(null=True, blank=True)
    resultado = models.CharField(max_length=50, null=True, blank=True)
    precision = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True, null=True)  # Agregar null=True

    class Meta:
        db_table = 'deteccion'

    def __str__(self):
        return f"Detección para DNI {self.dni_paciente} - {self.resultado}"


# Modelo para Análisis
class Analisis(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True, blank=True)
    subido_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'rol__nombre': 'Médico'})
    imagen = models.ImageField(upload_to='analisis/', null=True, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    es_benigno = models.BooleanField(null=True, blank=True)
    fecha_analisis = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    analizado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='analisis_realizados', limit_choices_to={'rol__nombre': 'Médico'})

    def __str__(self):
        resultado = "Benigno" if self.es_benigno else "Maligno"
        return f"Análisis de {self.paciente.nombres if self.paciente else 'Sin paciente'}: {resultado}"

# Modelo para Historial de Análisis
class Historial(models.Model):
    id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, db_column='paciente_id', null=True, blank=True)
    fecha_analisis = models.DateField(default=timezone.now, null=True, blank=True)
    imagen = models.TextField(blank=True, null=True)
    resultado = models.CharField(max_length=10, choices=[('Benigno', 'Benigno'), ('Maligno', 'Maligno')], default='Benigno', null=True, blank=True)
    realizado_por = models.CharField(max_length=100, blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'historial'

    def __str__(self):
        return f"Historial de {self.paciente.nombres if self.paciente else 'N/A'} - {self.fecha_analisis} - {self.resultado}"
