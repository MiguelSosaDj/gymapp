from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class Gimnasio(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre


class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    gimnasio = models.ForeignKey(Gimnasio, on_delete=models.CASCADE, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuarios_user_set_custom',
        blank=True,
        help_text='Los grupos a los que pertenece el usuario.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuarios_user_permissions_set_custom',
        blank=True,
        help_text='Permisos específicos para el usuario.'
    )

    def __str__(self):
        return self.username


class Alumno(models.Model):
    nombre = models.CharField(max_length=255, default="Desconocida", null=True, blank=True)
    telefono = models.CharField(max_length=20, default="Desconocida", null=True, blank=True)
    direccion = models.CharField(max_length=255, default="Desconocida", null=True, blank=True)
    gimnasio = models.ForeignKey(Gimnasio, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre


class Entrenamiento(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, null=True, blank=True)
    semana = models.PositiveIntegerField(null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, blank=True)
    tipo_entrenamiento = models.CharField(max_length=255, default="Default", null=True, blank=True)
    altura = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Progreso de {self.alumno.nombre} - Semana {self.semana}"


class BaseUserInfo(models.Model):
    gimnasio = models.ForeignKey(Gimnasio, on_delete=models.CASCADE, default=1)
    identificacion = models.CharField(max_length=20, default='Desconocido')
    nombre = models.CharField(max_length=100, default='Desconocido')
    edad = models.IntegerField(default=0)
    estatura = models.FloatField(default=0.0)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nombre


class LactanteInfo(BaseUserInfo):
    peso_actual = models.FloatField(default=0.0)
    peso_pregestacional = models.FloatField(default=0.0)
    imc_actual = models.FloatField(default=0.0)
    imc_cat = models.CharField(max_length=50, default='No calculado')
    dias_post_parto = models.IntegerField(default=0)
    retencion_post_parto = models.FloatField(default=0.0)
    retencion_post_parto_detalle = models.CharField(max_length=50, default='No calculado')
    tasa_metabolica = models.FloatField(default=0)
    factor_actividad_fisica = models.FloatField(default=1.4)
    descripcion_actividad_fisica = models.CharField(max_length=50, default='Ligero')
    requerimiento_energia = models.FloatField(default=0)
    energia_extra_requerida = models.FloatField(default=0)
    requerimiento_energia_total = models.FloatField(default=0)

    def __str__(self):
        return f'Lactante {self.nombre}'



class GestanteInfo(BaseUserInfo):
    # Otros campos existentes
    OPCIONES = [
        ('bajo_peso', 'Bajo peso'),
        ('adecuado', 'Adecuado'),
        ('sobrepeso', 'Sobrepeso'),
        ('obesidad', 'Obesidad'),
        ('adolescente', 'Adolescente'),
        ('gemelar', 'Gemelar'),
    ]
    
    seleccion_multiple = models.CharField(
        max_length=50,
        choices=OPCIONES,
        default='adecuado',
    )
    semana_gestacion = models.IntegerField(default=0)
    peso_actual = models.FloatField(default=0.0)
    peso_pregestacional = models.FloatField(default=0.0)
    imc_pregestacional = models.FloatField(default=0.0)
    imc_gestacional = models.FloatField(default=0.0)
    imc_pregestacional_cat = models.CharField(max_length=50, default='No calculado')

    def __str__(self):
        return self.nombre


class NinoInfo(BaseUserInfo):
    sexo = models.CharField(max_length=10, default='No especificado')
    peso = models.FloatField(default=0.0)
    talla = models.FloatField(default=0.0)
    perimetro_cefalico = models.FloatField(default=0.0)

    def __str__(self):
        return self.nombre


class NinoSanoInfo(models.Model):
    base_info = models.OneToOneField(NinoInfo, on_delete=models.CASCADE)
    alimentacion = models.CharField(max_length=255, default='No Aplica')
    pt = models.CharField(max_length=50, blank=True, null=True)
    te = models.CharField(max_length=50, blank=True, null=True)
    pce = models.CharField(max_length=50, blank=True, null=True)
    clasificacion_pt = models.CharField(max_length=50, blank=True, null=True)
    clasificacion_te = models.CharField(max_length=50, blank=True, null=True)
    clasificacion_pce = models.CharField(max_length=50, blank=True, null=True)
    ganancia_peso_gr = models.FloatField(default=0)
    calorias_1g_tejido = models.FloatField(default=0)
    veces_que_gane = models.IntegerField(default=1)
    calorias_crecimiento = models.FloatField(default=0)
    ajuste_deficit = models.FloatField(default=0)
    kcal_totales = models.FloatField(default=0)
    leche_materna_exclusiva = models.FloatField(default=0)
    formula_infantil = models.FloatField(default=0)
    leche_materna_y_formula = models.FloatField(default=0)
    rango_1_18_anos = models.FloatField(default=0)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Información Nutricional de {self.base_info.nombre}'


class BajoPesoInfo(models.Model):
    base_info = models.OneToOneField(GestanteInfo, on_delete=models.CASCADE)

    # Datos calculados relacionados al peso
    imc_saludable = models.FloatField(default=0.0)
    peso_pregestacional_saludable = models.FloatField(default=0.0)
    gramos_semana = models.FloatField(default=0.0)
    ganancia_1_trimestre = models.FloatField(default=2.0)
    ganancia_2_y_3_trimestre_gramos = models.FloatField(default=0.0)
    ganancia_2_y_3_trimestre_kg = models.FloatField(default=0.0)
    ganancia_total = models.FloatField(default=0.0)
    peso_total_embarazo = models.FloatField(default=0.0)
    imc_semana_40 = models.FloatField(default=0.0)

    # Ruta de % de peso pregestacional saludable
    ganancia_peso_embarazo = models.FloatField(default=0.0)
    ganancia_2_y_3_trimestre_parte2 = models.FloatField(default=0.0)
    peso_total_parte2 = models.FloatField(default=0.0)
    imc_semana_40_parte2 = models.FloatField(default=0.0)

    # Evaluación de ganancia de peso
    ganado = models.FloatField(default=0.0)
    debio_ganar = models.FloatField(default=0.0)

    # Reprogramación
    peso_a_ganar = models.FloatField(default=0.0)
    semanas_faltantes = models.IntegerField(default=0)
    gramos_por_semana = models.FloatField(default=0.0)
    clasificacion_peso = models.CharField(max_length=50, default="Adecuado")

    # Requerimiento de energía
    tasa_metabolica = models.FloatField(default=0.0)
    factor_actividad_fisica = models.FloatField(default=1.4)
    requerimiento_energia_total = models.FloatField(default=0.0)

    # Aporte proteico
    metodo1_g_dia = models.FloatField(default=0.0)
    metodo1_kcal = models.FloatField(default=0.0)
    metodo1_amdr = models.FloatField(default=0.0)
    metodo2_g_dia = models.FloatField(default=0.0)
    metodo2_kcal = models.FloatField(default=0.0)
    metodo2_amdr = models.FloatField(default=0.0)

    def __str__(self):
        return f'Bajo Peso - {self.base_info.nombre}'
