from rest_framework import serializers
from .models import Usuario, Alumno, Entrenamiento

# Serializador para el modelo Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'gimnasio', 'rol']

# Serializador para el modelo Alumno
class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ['id', 'nombre', 'telefono', 'direccion']

# Serializador para el modelo Entrenamiento
class EntrenamientoSerializer(serializers.ModelSerializer):
    alumno = AlumnoSerializer(read_only=True)  # Mostrar datos del alumno en el entrenamiento
    
    class Meta:
        model = Entrenamiento
        fields = ['id', 'alumno', 'semana', 'peso', 'tipo_entrenamiento', 'altura']

from .models import NinoInfo, LactanteInfo, GestanteInfo

class NinoInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NinoInfo
        fields = '__all__'

class LactanteInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LactanteInfo
        fields = '__all__'

    def create(self, validated_data):
        # Verifica que este mensaje se imprima
        print("Entrando en el método create del serializador")

        # Cálculo de IMC
        peso_actual = validated_data.get('peso_actual')
        estatura = validated_data.get('estatura')
        imc_actual = peso_actual / (estatura ** 2)

        # Clasificación de IMC
        if imc_actual < 20:
            imc_clasificacion = "Bajo peso"
        elif imc_actual < 24.9:
            imc_clasificacion = "Normal"
        elif imc_actual < 29.9:
            imc_clasificacion = "Sobrepeso"
        else:
            imc_clasificacion = "Obesidad"

        # Cálculo de Retención Post Parto
        peso_pregestacional = validated_data.get('peso_pregestacional')
        retencion_post_parto = peso_actual - peso_pregestacional

        # Agregar valores calculados a validated_data
        validated_data['imc_actual'] = imc_clasificacion
        validated_data['retencion_post_parto'] = retencion_post_parto

        # Crear la instancia del modelo con los datos calculados
        return LactanteInfo.objects.create(**validated_data)


class GestanteInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GestanteInfo
        fields = '__all__'
