from django.db import models
from datetime import date

class Medico(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    cedula = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=20)
    horario = models.CharField(max_length=100, default="08:00 - 16:00")
    usuario = models.CharField(max_length=50, default="medico")
    password = models.CharField(max_length=50, default="1234")

    def __str__(self):
        return f"Dr(a). {self.nombre} ({self.especialidad})"


class Personal(models.Model):
    ROLES = (
        ('recepcion', '📋 Recepcionista'),
        ('enfermeria', '💉 Enfermería'),
        ('soporte', '🛠️ Soporte Técnico'),
    )
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=20, choices=ROLES)
    usuario = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    horario = models.CharField(max_length=100, default="08:00 - 16:00") 

    def __str__(self):
        return f"{self.nombre} - {self.get_rol_display()}"


class Paciente(models.Model):
    GENEROS = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Otro', 'Otro')
    ]
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)
    curp = models.CharField(max_length=18, unique=True)
    telefono = models.CharField(max_length=10)
    tipo_sangre = models.CharField(max_length=5)
    
    edad = models.PositiveIntegerField(null=True, blank=True)
    genero = models.CharField(max_length=15, choices=GENEROS, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"


class Cita(models.Model):
    ESTADOS = [
        ('En Espera', 'En Espera'),
        ('Espera Extra (Emergencia)', 'Espera Extra (Emergencia)'),
        ('En Consulta', 'En Consulta'),
        ('Finalizada', 'Finalizada')
    ]
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today)
    hora = models.TimeField()
    motivo = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=40, choices=ESTADOS, default='En Espera')

    def __str__(self):
        return f"{self.hora} - {self.paciente.nombre} con {self.medico.nombre}"


class SignoVital(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='signos')
    presion = models.CharField(max_length=20) 
    temperatura = models.CharField(max_length=10) 
    peso = models.CharField(max_length=10) 
    estatura = models.CharField(max_length=10) 
    oxigenacion = models.CharField(max_length=10, blank=True, null=True) 
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Signos de {self.paciente.nombre} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"


class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    medico_nombre = models.CharField(max_length=100, default="Dr. General")
    diagnostico = models.TextField()
    receta = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consulta {self.paciente.nombre} - {self.fecha.strftime('%d/%m/%Y')}"


class TicketSoporte(models.Model):
    empleado = models.CharField(max_length=100)
    area = models.CharField(max_length=50, default="General")
    falla = models.TextField()
    estado = models.CharField(max_length=20, default="Pendiente")
    fecha = models.DateTimeField(auto_now_add=True)
    resuelto_por = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Falla en {self.area} reportada por {self.empleado} - {self.estado}"