from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.db.models import Subquery, OuterRef
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import NinoInfo, LactanteInfo, GestanteInfo, Gimnasio, Usuario, Entrenamiento, Alumno, NinoSanoInfo, BajoPesoInfo, SobrePesoInfo
from .serializers import LactanteInfoSerializer, GestanteInfoSerializer, NinoInfoSerializer, AlumnoSerializer, EntrenamientoSerializer
from rest_framework.decorators import api_view

class HomeDataView(APIView):
    authentication_classes = []  # Quitar JWTAuthentication temporalmente
    permission_classes = []  # Quitar IsAuthenticated temporalmente
    
    def get(self, request):
        

# Para LactanteInfo
        latest_lactante_info = LactanteInfo.objects.filter(
            identificacion=OuterRef('identificacion')
        ).order_by('-id')

        lactante_info = LactanteInfo.objects.filter(
            id=Subquery(latest_lactante_info.values('id')[:1])
        ).distinct('identificacion')

        # Para GestanteInfo
        

        latest_gestante_info = GestanteInfo.objects.filter(
            identificacion=OuterRef('identificacion')
        ).order_by('-id')
        gestante_info = GestanteInfo.objects.filter(
            id=Subquery(latest_gestante_info.values('id')[:1])
        ).distinct('identificacion')

        # Para NinoInfo miguel sosa
        latest_nino_info = NinoInfo.objects.filter(
            identificacion=OuterRef('identificacion')
        ).order_by('-id')

        nino_info = NinoInfo.objects.filter(
            id=Subquery(latest_nino_info.values('id')[:1])
        ).distinct('identificacion')
        
        

        data = {
            'lactante_info': LactanteInfoSerializer(lactante_info, many=True).data,
            'gestante_info': GestanteInfoSerializer(gestante_info, many=True).data,
            'nino_info': NinoInfoSerializer(nino_info, many=True).data,
        }

        return Response(data, status=status.HTTP_200_OK)


class PersonasView(APIView):
    authentication_classes = []  # Quitar JWTAuthentication temporalmente
    permission_classes = []  # Quitar IsAuthenticated temporalmente
    
    def get(self, request):
        persona_id = request.query_params.get('persona', None)

        lactante_info = []
        gestante_info = []
        nino_info = []
        

        # Si se proporciona un ID de persona, filtra los datos
        if persona_id is not None:
            lactante_info = LactanteInfo.objects.filter(id=persona_id)
            gestante_info = GestanteInfo.objects.filter(id=persona_id)
            nino_info = NinoInfo.objects.filter(id=persona_id)
        else:
            # Si no hay un ID de persona, devolver todos los datos (opcional)
            lactante_info = LactanteInfo.objects.all()
            gestante_info = GestanteInfo.objects.all()
            nino_info = NinoInfo.objects.all()

        data = {
            'lactante_info': LactanteInfoSerializer(lactante_info, many=True).data,
            'gestante_info': GestanteInfoSerializer(gestante_info, many=True).data,
            'nino_info': NinoInfoSerializer(nino_info, many=True).data,
        }

        return Response(data, status=status.HTTP_200_OK)


class LoginView(APIView):
    authentication_classes = []  # Quitar JWTAuthentication temporalmente
    permission_classes = []  # Quitar IsAuthenticated temporalmente
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
            })
        return Response({'error': 'Credenciales inválidas'}, status=401)
    
    def get(self, request):
        # Aquí puedes devolver alguna información útil o indicar que el método GET no es soportado
        return Response({'detail': 'Este endpoint es para autenticación mediante POST.'}, status=200)


class SaveNinoInfo(APIView):
    authentication_classes = []  # Quitar JWTAuthentication temporalmente
    permission_classes = []  # Quitar IsAuthenticated temporalmente
    
    def post(self, request):
        
        try:
            gimnasio = Gimnasio.objects.get(id=1)
            nombre = request.data.get('nombre')
            edad = int(request.data.get('edad'))
            identification = request.data.get('identification')
            sexo = request.data.get('sexo')
            talla = float(request.data.get('talla'))
            peso = float(request.data.get('peso'))
            perimetro_cefalico = float(request.data.get('perimetro_cefalico'))

            nino_info = NinoInfo.objects.create(
                gimnasio=gimnasio,
                nombre=nombre,
                edad=edad,
                sexo=sexo,
                identificacion=identification,
                talla=talla,
                peso=peso,
                perimetro_cefalico=perimetro_cefalico,
            )

            return Response({"message": "Información de niño guardada exitosamente"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Gimnasio, LactanteInfo

class SaveLactanteInfo(APIView):
    authentication_classes = []  # Quitar JWTAuthentication temporalmente
    permission_classes = []  # Quitar IsAuthenticated temporalmente
    def post(self, request):
        
        try:
            gimnasio = Gimnasio.objects.get(id=1)
            nombre = request.data.get('nombre')
            edad = int(request.data.get('edad'))
            estatura = float(request.data.get('estatura'))
            peso_actual = float(request.data.get('peso_actual'))
            peso_pregestacional = float(request.data.get('peso_pregestacional'))
            dias_post_parto = int(request.data.get('dias_post_parto'))
            identification = request.data.get('identification')

            
            # Nuevo campo de energía extra requerida
            energia_extra_requerida = request.data.get('energia_extra_requerida')
            imc_actual = peso_actual / ((estatura/100) ** 2)
            if imc_actual < 20:
                imc_clasificacion = "Bajo peso"
            elif imc_actual < 24.9:
                imc_clasificacion = "Normal"
            elif imc_actual < 29.9:
                imc_clasificacion = "Sobrepeso"
            else:
                imc_clasificacion = "Obesidad"

            retencion_post_parto = peso_actual - peso_pregestacional

            lactante_info = LactanteInfo.objects.create(
                gimnasio=gimnasio,
                nombre=nombre,
                edad=edad,
                identificacion=identification,
                estatura=estatura,
                peso_actual=peso_actual,
                peso_pregestacional=peso_pregestacional,
                imc_actual=imc_actual,
                imc_cat=imc_clasificacion,
                dias_post_parto=dias_post_parto,
                retencion_post_parto=retencion_post_parto,
                retencion_post_parto_detalle=energia_extra_requerida,  # Guardar energía extra requerida
            )

            return Response({"message": "Información de lactante guardada exitosamente"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class SaveGestanteInfo(APIView):
    authentication_classes = []  # Quitar JWTAuthentication temporalmente
    permission_classes = []  # Quitar IsAuthenticated temporalmente
    def post(self, request):
        
        try:
            gimnasio = Gimnasio.objects.get(id=1)
            nombre = request.data.get('nombre')
            edad = int(request.data.get('edad'))
            estatura = float(request.data.get('estatura'))/100
            semana_gestacion = int(request.data.get('semana_gestacion'))
            
            peso_actual = float(request.data.get('peso_actual'))
            peso_pregestacional = float(request.data.get('peso_pregestacional'))
            identification = request.data.get('identification')

            imc_pregestacional = peso_pregestacional / ((estatura) ** 2)
            imc_gestacional = peso_actual / (estatura ** 2)

            if imc_pregestacional < 20:
                imc_pre_clasificacion = "Bajo peso"
            elif imc_pregestacional < 24.9:
                imc_pre_clasificacion = "Normal"
            elif imc_pregestacional < 29.9:
                imc_pre_clasificacion = "Sobrepeso"
            else:
                imc_pre_clasificacion = "Obesidad"

            gestante_info = GestanteInfo.objects.create(
                gimnasio=gimnasio,
                nombre=nombre,
                edad=edad,
                identificacion=identification,
                estatura=estatura,
                semana_gestacion=semana_gestacion,
                peso_actual=peso_actual,
                peso_pregestacional=peso_pregestacional,
                imc_pregestacional=imc_pregestacional,
                imc_gestacional=imc_gestacional,
                imc_pregestacional_cat=imc_pre_clasificacion,
                seleccion_multiple=request.data.get('seleccion_multiple', 'adecuado')  # Save the dropdown selection
            )
            gestante_info.save()

            return Response({"message": "Información de gestante guardada exitosamente"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
@method_decorator(csrf_exempt, name='dispatch')
class UserInfoView(APIView):
    def get(self, request):
        

        try:
            user = request.user
            tipo_usuario = request.query_params.get('tipo')
            if tipo_usuario == 'gestante':
                gestante_info = get_object_or_404(GestanteInfo, gimnasio__usuario=user)
                data = {
                    "nombre": gestante_info.nombre,
                    "edad": gestante_info.edad,
                    "estatura": gestante_info.estatura,
                    "semana_gestacion": gestante_info.semana_gestacion,
                    "peso_actual": gestante_info.peso_actual,
                    "imc_pregestacional": gestante_info.imc_pregestacional,
                    "imc_gestacional": gestante_info.imc_gestacional,
                    "tipo": "gestante"
                }
            elif tipo_usuario == 'lactante':
                lactante_info = get_object_or_404(LactanteInfo, gimnasio__usuario=user)
                data = {
                    "nombre": lactante_info.nombre,
                    "edad": lactante_info.edad,
                    "estatura": lactante_info.estatura,
                    "peso_actual": lactante_info.peso_actual,
                    "imc_actual": lactante_info.imc_actual,
                    "dias_post_parto": lactante_info.dias_post_parto,
                    "retencion_post_parto": lactante_info.retencion_post_parto,
                    "tipo": "lactante"
                }
            elif tipo_usuario == 'niño':
                nino_info = get_object_or_404(NinoInfo, gimnasio__usuario=user)
                data = {
                    "nombre": nino_info.nombre,
                    "edad": nino_info.edad,
                    "sexo": nino_info.sexo,
                    "talla": nino_info.talla,
                    "peso": nino_info.peso,
                    "perimetro_cefalico": nino_info.perimetro_cefalico,
                    "tipo": "niño"
                }
            else:
                return Response({"error": "Tipo de usuario no especificado o inválido"}, status=status.HTTP_400_BAD_REQUEST)

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ListUsuariosView(APIView):
    def get(self, request):
        

        tipo_usuario = request.query_params.get('tipo')
        
        if tipo_usuario == 'gestante':
            gestantes = GestanteInfo.objects.all()
            data = [{
                "nombre": gestante.nombre,
                "edad": gestante.edad,
                "estatura": gestante.estatura,
                "semana_gestacion": gestante.semana_gestacion,
                "peso_actual": gestante.peso_actual,
                "imc_pregestacional": gestante.imc_pregestacional,
                "imc_gestacional": gestante.imc_gestacional,
            } for gestante in gestantes]
        elif tipo_usuario == 'lactante':
            lactantes = LactanteInfo.objects.all()
            data = [{
                "nombre": lactante.nombre,
                "edad": lactante.edad,
                "estatura": lactante.estatura,
                "peso_actual": lactante.peso_actual,
                "imc_actual": lactante.imc_actual,
                "dias_post_parto": lactante.dias_post_parto,
                "retencion_post_parto": lactante.retencion_post_parto,
            } for lactante in lactantes]
        elif tipo_usuario == 'niño':
            ninos = NinoInfo.objects.all()
            data = [{
                "nombre": nino.nombre,
                "edad": nino.edad,
                "sexo": nino.sexo,
                "talla": nino.talla,
                "peso": nino.peso,
                "perimetro_cefalico": nino.perimetro_cefalico,
            } for nino in ninos]
        else:
            return Response({"error": "Tipo de usuario no especificado o inválido"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_200_OK)


class AlumnoViewSet(viewsets.ModelViewSet):

    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    authentication_classes = []  # Quitar JWTAuthentication temporalmente
    permission_classes = []  # Quitar IsAuthenticated temporalmente

    def list(self, request, *args, **kwargs):
        alumnos = Alumno.objects.all()
        data = []
        for alumno in alumnos:
            alumno_data = AlumnoSerializer(alumno).data
            data.append(alumno_data)
        return Response(data)

    def create(self, request, *args, **kwargs):
        # Obtener los datos del request
        

        nombre = request.data.get('nombre')
        telefono = request.data.get('telefono')
        direccion = request.data.get('direccion')

        # Crear el alumno
        alumno = Alumno(nombre=nombre, telefono=telefono, direccion=direccion)
        alumno.save()

        # Responder con los detalles del alumno creado
        return JsonResponse({'id': alumno.id, 'nombre': alumno.nombre, 'telefono': alumno.telefono, 'direccion': alumno.direccion}, status=201)
    

class EntrenamientoViewSet(viewsets.ModelViewSet):
    queryset = Entrenamiento.objects.all()
    serializer_class = EntrenamientoSerializer
    authentication_classes = []  # Quitar JWTAuthentication temporalmente
    permission_classes = []  # Quitar IsAuthenticated temporalmente

    def list(self, request, *args, **kwargs):
        

        alumno_id = request.query_params.get('alumno', None)

        if alumno_id is not None:
            entrenamientos = Entrenamiento.objects.filter(alumno_id=alumno_id)
        else:
            entrenamientos = Entrenamiento.objects.all()

        data = EntrenamientoSerializer(entrenamientos, many=True).data
        return Response(data)

    def create(self, request, *args, **kwargs):
        # Buscar el alumno por ID
        alumno_id = request.data.get('alumno_id')
        if not alumno_id:
            return JsonResponse({'error': 'alumno_id no proporcionado'}, status=400)

        try:
            alumno = Alumno.objects.get(id=alumno_id)
        except Alumno.DoesNotExist:
            return JsonResponse({'error': 'Alumno no encontrado'}, status=404)

        # Calcular la próxima semana (una más que la última semana registrada)
        ultimo_entrenamiento = Entrenamiento.objects.filter(alumno=alumno).order_by('semana').last()
        nueva_semana = ultimo_entrenamiento.semana + 1 if ultimo_entrenamiento else 1

        # Obtener los datos del request
        peso = request.data.get('peso')
        tipo_entrenamiento = request.data.get('tipo_entrenamiento')
        altura = request.data.get('altura')

        # Crear el entrenamiento
        entrenamiento = Entrenamiento(
            alumno=alumno,
            semana=nueva_semana,
            peso=peso,
            tipo_entrenamiento=tipo_entrenamiento,
            altura=altura
        )
        entrenamiento.save()

        # Responder con los detalles del entrenamiento creado
        return JsonResponse({
            'id': entrenamiento.id,
            'alumno': entrenamiento.alumno.nombre,
            'semana': entrenamiento.semana,
            'peso': entrenamiento.peso,
            'tipo_entrenamiento': entrenamiento.tipo_entrenamiento,
            'altura': entrenamiento.altura
        }, status=201)


class NinoInfoView(View):
    authentication_classes = []  # Quitar JWTAuthentication temporalmente
    permission_classes = []  # Quitar IsAuthenticated temporalmente
    def get(self, request, nino_id):
        
        try:
            # Obtener la información del niño con el ID proporcionado
            nino_info = NinoInfo.objects.get(id=nino_id)
            data = {
                "id": nino_info.id,
                "nombre": nino_info.nombre,
                "sexo": nino_info.sexo,
                "edad": nino_info.edad,
                "talla": nino_info.talla,
                "peso": nino_info.peso,
                "perimetro_cefalico": nino_info.perimetro_cefalico,
            }
            return JsonResponse(data, status=200)
        except NinoInfo.DoesNotExist:
            return JsonResponse({"error": "Niño no encontrado"}, status=404)

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class NinoSanoView(APIView):
    authentication_classes = []  # Quitar JWTAuthentication temporalmente
    permission_classes = []  # Quitar IsAuthenticated temporalmente

    def post(self, request):
        try:
            # Cargar el cuerpo de la solicitud
            data = json.loads(request.body)
            
            # Obtener los datos del niño con base en el ID del niño
            base_info = NinoInfo.objects.get(id=data['base_info_id'])
            
            # Crear o actualizar la información de NinoSanoInfo
            nino_sano_info, created = NinoSanoInfo.objects.get_or_create(base_info=base_info)
            
            # Actualizamos los campos con la información del request
            nino_sano_info.alimentacion = data.get('alimentacion', 'No Aplica')
            nino_sano_info.pt = data.get('pt', '')
            nino_sano_info.te = data.get('te', '')
            nino_sano_info.pce = data.get('pce', '')
            nino_sano_info.clasificacion_pt = data.get('clasificacion_pt', '')
            nino_sano_info.clasificacion_te = data.get('clasificacion_te', '')
            nino_sano_info.clasificacion_pce = data.get('clasificacion_pce', '')

            # Convertir valores a flotante o entero antes de hacer los cálculos
            nino_sano_info.ganancia_peso_gr = float(data.get('ganancia_peso_gr', 0))
            nino_sano_info.calorias_1g_tejido = float(data.get('calorias_1g_tejido', 0))
            nino_sano_info.veces_que_gane = int(data.get('veces_que_gane', 1))

            # Cálculo de calorías para crecimiento (si es que no viene directamente)
            calorias_crecimiento = data.get('calorias_crecimiento', None)
            if calorias_crecimiento is None:
                calorias_crecimiento = float(nino_sano_info.ganancia_peso_gr) * float(nino_sano_info.calorias_1g_tejido)
            nino_sano_info.calorias_crecimiento = calorias_crecimiento

            # Cálculo de ajuste por déficit (si es que no viene directamente)
            ajuste_deficit = data.get('ajuste_deficit', None)
            if ajuste_deficit is None:
                ajuste_deficit = calorias_crecimiento * nino_sano_info.veces_que_gane * 5
            nino_sano_info.ajuste_deficit = ajuste_deficit

            # Cálculo de calorías totales
            kcal_totales = data.get('kcal_totales', None)
            if kcal_totales is None:
                kcal_totales = calorias_crecimiento + ajuste_deficit
            nino_sano_info.kcal_totales = kcal_totales

            # Nuevos campos añadidos
            nino_sano_info.leche_materna_exclusiva = float(data.get('leche_materna_exclusiva', 0))
            nino_sano_info.formula_infantil = float(data.get('formula_infantil', 0))
            nino_sano_info.leche_materna_y_formula = float(data.get('leche_materna_y_formula', 0))
            nino_sano_info.rango_1_18_anos = float(data.get('rango_1_18_anos', 0))
            
            # Guardar la información
            nino_sano_info.save()

            return Response({"message": "Datos guardados correctamente"}, status=status.HTTP_200_OK)
        except NinoInfo.DoesNotExist:
            return Response({"error": "Niño no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, nino_id):
        try:
            # Buscar la información nutricional del niño
            nino_sano_info = NinoSanoInfo.objects.get(base_info_id=nino_id)
            
            # Crear la respuesta con toda la información relevante
            data = {
                'alimentacion': nino_sano_info.alimentacion,
                'pt': nino_sano_info.pt,
                'te': nino_sano_info.te,
                'pce': nino_sano_info.pce,
                'clasificacion_pt': nino_sano_info.clasificacion_pt,
                'clasificacion_te': nino_sano_info.clasificacion_te,
                'clasificacion_pce': nino_sano_info.clasificacion_pce,
                'ganancia_peso_gr': nino_sano_info.ganancia_peso_gr,
                'calorias_1g_tejido': nino_sano_info.calorias_1g_tejido,
                'calorias_crecimiento': nino_sano_info.calorias_crecimiento,
                'veces_que_gane': nino_sano_info.veces_que_gane,
                'ajuste_deficit': nino_sano_info.ajuste_deficit,
                'kcal_totales': nino_sano_info.kcal_totales,
                # Nuevos campos añadidos
                'leche_materna_exclusiva': nino_sano_info.leche_materna_exclusiva,
                'formula_infantil': nino_sano_info.formula_infantil,
                'leche_materna_y_formula': nino_sano_info.leche_materna_y_formula,
                'rango_1_18_anos': nino_sano_info.rango_1_18_anos
            }

            return Response(data, status=status.HTTP_200_OK)
        except NinoSanoInfo.DoesNotExist:
            return Response({"error": "Información de nutrición no encontrada"}, status=status.HTTP_404_NOT_FOUND)

@method_decorator(csrf_exempt, name='dispatch')
class LactanteView(APIView):
    authentication_classes = []  # Quitar JWTAuthentication temporalmente
    permission_classes = []  # Quitar IsAuthenticated temporalmente

    def post(self, request):
        try:

            data = json.loads(request.body)

            # Realizar cálculos de tasa metabólica y requerimiento energético
            edad = int(data.get('edad'))
            peso_actual = float(data.get('peso_actual'))
            retencion_post_parto = float(data.get('retencion_post_parto'))
            retencion_post_parto_detalle = data.get('retencion_post_parto_detalle')
            
            factor_actividad_fisica = float(data.get('factor_actividad_fisica'))

            # Cálculo de tasa metabólica
            if edad < 30:
                tasa_metabolica = (14.818 * peso_actual) + 486.6
            else:
                tasa_metabolica = (8.126 * peso_actual) + 845.6

         
            if retencion_post_parto_detalle == "Inadecuado":
                energia_extra_requerida = 675
            elif retencion_post_parto_detalle == "Adecuado":
                energia_extra_requerida = 500
            else:
                energia_extra_requerida = 0
            imc_actual = float(data.get('imc_actual'))
            if imc_actual < 20:
                imc_clasificacion = "Bajo peso"
            elif imc_actual < 24.9:
                imc_clasificacion = "Normal"
            elif imc_actual < 29.9:
                imc_clasificacion = "Sobrepeso"
            else:
                imc_clasificacion = "Obesidad"
            if factor_actividad_fisica <= 1.69:
                descripcion_actividad_fisica = 'Ligero'
            elif factor_actividad_fisica > 1.69 and factor_actividad_fisica <= 1.99:
                descripcion_actividad_fisica = 'Moderado'
            elif factor_actividad_fisica > 1.99 and factor_actividad_fisica <= 2.4:
                descripcion_actividad_fisica = 'Fuerte'

            
            # Crear o actualizar la información de LactanteInfo
            lactante_info = LactanteInfo.objects.create(
                nombre=data.get('nombre'),
                identificacion=data.get('identificacion'),
                edad=edad,
                estatura=float(data.get('estatura')),
                peso_actual=peso_actual,
                peso_pregestacional=float(data.get('peso_pregestacional')),
                imc_actual=float(data.get('imc_actual')),
                dias_post_parto=int(data.get('dias_post_parto')),
                retencion_post_parto=retencion_post_parto,
                retencion_post_parto_detalle=retencion_post_parto_detalle,
                imc_cat=imc_clasificacion,
                tasa_metabolica=tasa_metabolica,
                factor_actividad_fisica=factor_actividad_fisica,
                descripcion_actividad_fisica=descripcion_actividad_fisica,
                requerimiento_energia=float(data.get('requerimiento_energia')),
                energia_extra_requerida=energia_extra_requerida,
                requerimiento_energia_total=float(data.get('requerimiento_total_energia')),
            )

            lactante_info.save()

            return Response({"message": "Datos guardados correctamente"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, lactante_id):
        try:
            lactante_info = LactanteInfo.objects.latest('id')
            data = {
                "nombre": lactante_info.nombre,
                "edad": lactante_info.edad,
                "estatura": lactante_info.estatura,
                "peso_actual": lactante_info.peso_actual,
                "peso_pregestacional": lactante_info.peso_pregestacional,
                "imc_actual": lactante_info.imc_actual,
                "dias_post_parto": lactante_info.dias_post_parto,
                "retencion_post_parto": lactante_info.retencion_post_parto,
                "retencion_post_parto_detalle": lactante_info.retencion_post_parto_detalle,
                "tasa_metabolica": lactante_info.tasa_metabolica,
                "factor_actividad_fisica": lactante_info.factor_actividad_fisica,
                "descripcion_actividad_fisica": lactante_info.descripcion_actividad_fisica,
                "requerimiento_energia": lactante_info.requerimiento_energia,
                "energia_extra_requerida": lactante_info.energia_extra_requerida,
                "requerimiento_energia_total": lactante_info.requerimiento_energia_total,
            }
            return Response(data, status=status.HTTP_200_OK)
        except LactanteInfo.DoesNotExist:
            return Response({"error": "Información de lactante no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        

@method_decorator(csrf_exempt, name='dispatch')
class GestanteView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            data = json.loads(request.body)
            

            # Obtener o crear la información básica de la gestante
            gestante_info = GestanteInfo.objects.create(
                identificacion=data.get('identificacion'),
                nombre=data.get('nombre'),
                edad=data.get('edad'),
                estatura=data.get('estatura'),
                peso_actual=data.get('peso_actual'),
                peso_pregestacional=data.get('peso_pregestacional'),
                imc_pregestacional=data.get('imc_pregestacional'),
                imc_gestacional=data.get('imc_gestacional'),
                semana_gestacion=data.get('semana_gestacion'),
                seleccion_multiple=data.get('clasificacion_peso', 'bajo_peso'),
            )

            bajo_peso_info = BajoPesoInfo.objects.create(
                base_info=gestante_info,
                # Título 2
                imc_saludable=data.get('imc_saludable', 0.0),
                peso_pregestacional_saludable=data.get('peso_pregestacional_saludable', 0.0),

                # Título 3
                gramos_semana=data.get('gramos_semana', 0.0),
                ganancia_1_trimestre=data.get('ganancia_1_trimestre', 0.0),
                ganancia_2_y_3_trimestre_gramos=data.get('ganancia_2_y_3_trimestre_gramos', 0.0),
                ganancia_2_y_3_trimestre_kg=data.get('ganancia_2_y_3_trimestre_kg', 0.0),
                peso_total_embarazo=data.get('peso_total_embarazo', 0.0),
                peso_final=data.get('peso_final', 0.0),  # Campo agregado que faltaba

                # Título 4
                ganancia_peso_embarazo=data.get('ganancia_peso_embarazo', 0.0),
                ganancia_peso_clasificacion=data.get('ganancia_peso_clasificacion', 'Adecuado'),
                ganancia_primer_trimestre=data.get('ganancia_primer_trimestre', 0.0),
                ganancia_2y3_trimestre_gsem=data.get('ganancia_2y3_trimestre_gsem', 0.0),
                peso_total_embarazo_titulo_4=data.get('peso_total_embarazo_titulo_4', 0.0),
                imc_semana_40=data.get('imc_semana_40', 0.0),

                # Título 5
                ganancia_tipo=data.get('ganancia_tipo', 'g/sem'),
                gano=data.get('gano', 0.0),
                debio_ganar=data.get('debio_ganar', 0.0),

                # Título 6
                peso_a_ganar=data.get('peso_a_ganar', 0.0),
                semanas_faltantes=data.get('semanas_faltantes', 0),
                gramos_por_semana=data.get('gramos_por_semana', 0.0),
                clasificacion_gramos=data.get('clasificacion_gramos', 'Adecuado'),

                # Título 7
                tasa_metabolica=data.get('tasa_metabolica', 0.0),
                factor_actividad_fisica=data.get('factor_actividad_fisica', 1.4),
                requerimiento_energia_total=data.get('requerimiento_energia_total', 0.0),
                adicion_gestante=data.get('adicion_gestante', 0.0),  # Campo agregado que faltaba
                total_energia_adicion=data.get('total_energia_adicion', 0.0),  # Campo agregado que faltaba

                # Título 8
                metodo1_g_dia=data.get('metodo1_g_dia', 0.0),
                metodo1_kcal=data.get('metodo1_kcal', 0.0),
                metodo1_amdr=data.get('metodo1_amdr', 0.0),
                metodo2_g_dia=data.get('metodo2_g_dia', 0.0),
                metodo2_kcal=data.get('metodo2_kcal', 0.0),
                metodo2_amdr=data.get('metodo2_amdr', 0.0),
            )

            return Response({"message": "Datos guardados correctamente"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, gestante_id):
        
        try:
            # Buscar la información de la gestante
            gestante_info = GestanteInfo.objects.get(id=gestante_id)
            bajo_peso_info = BajoPesoInfo.objects.get(base_info=gestante_info)

            # Crear la respuesta con toda la información relevante
            data = {
                'gestante_info': {
                    'nombre': gestante_info.nombre,
                    'edad': gestante_info.edad,
                    'estatura': gestante_info.estatura,
                    'peso_actual': gestante_info.peso_actual,
                    'peso_pregestacional': gestante_info.peso_pregestacional,
                    'imc_pregestacional': gestante_info.imc_pregestacional,
                    'imc_gestacional': gestante_info.imc_gestacional,
                    'semana_gestacion': gestante_info.semana_gestacion,
                    'seleccion_multiple': gestante_info.seleccion_multiple
                },
                'bajo_peso_info': {
                    'imc_saludable': bajo_peso_info.imc_saludable,
                    'peso_pregestacional_saludable': bajo_peso_info.peso_pregestacional_saludable,
                    'gramos_semana': bajo_peso_info.gramos_semana,
                    'ganancia_1_trimestre': bajo_peso_info.ganancia_1_trimestre,
                    'ganancia_2_y_3_trimestre_gramos': bajo_peso_info.ganancia_2_y_3_trimestre_gramos,
                    'ganancia_2_y_3_trimestre_kg': bajo_peso_info.ganancia_2_y_3_trimestre_kg,
                    'ganancia_total': bajo_peso_info.ganancia_total,
                    'peso_total_embarazo': bajo_peso_info.peso_total_embarazo,
                    'imc_semana_40': bajo_peso_info.imc_semana_40,
                    'ganancia_peso_embarazo': bajo_peso_info.ganancia_peso_embarazo,
                    'ganancia_2_y_3_trimestre_parte2': bajo_peso_info.ganancia_2_y_3_trimestre_parte2,
                    'peso_total_parte2': bajo_peso_info.peso_total_parte2,
                    'imc_semana_40_parte2': bajo_peso_info.imc_semana_40_parte2,
                    'tasa_metabolica': bajo_peso_info.tasa_metabolica,
                    'factor_actividad_fisica': bajo_peso_info.factor_actividad_fisica,
                    'requerimiento_energia_total': bajo_peso_info.requerimiento_energia_total,
                    'metodo1_g_dia': bajo_peso_info.metodo1_g_dia,
                    'metodo1_kcal': bajo_peso_info.metodo1_kcal,
                    'metodo1_amdr': bajo_peso_info.metodo1_amdr,
                    'metodo2_g_dia': bajo_peso_info.metodo2_g_dia,
                    'metodo2_kcal': bajo_peso_info.metodo2_kcal,
                    'metodo2_amdr': bajo_peso_info.metodo2_amdr,
                    'ganado': bajo_peso_info.ganado,
                    'debio_ganar': bajo_peso_info.debio_ganar,
                    'peso_a_ganar': bajo_peso_info.peso_a_ganar,
                    'gramos_por_semana': bajo_peso_info.gramos_por_semana,
                    'clasificacion_peso': bajo_peso_info.clasificacion_peso,
                }
            }

            return Response(data, status=status.HTTP_200_OK)

        except (GestanteInfo.DoesNotExist, BajoPesoInfo.DoesNotExist):
            return Response({"error": "Gestante no encontrada"}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(csrf_exempt, name='dispatch')
class SobrePesoView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            data = json.loads(request.body)

            # Título 1: Datos personales
              # Obtener o crear la información básica de la gestante
            
            gestante_info = GestanteInfo.objects.create(
                identificacion=data.get('identificacion'),
                nombre=data.get('nombre'),
                edad=data.get('edad'),
                estatura=data.get('estatura'),
                peso_actual=data.get('peso_actual'),
                peso_pregestacional=data.get('peso_pregestacional'),
                imc_pregestacional=data.get('imc_pregestacional'),
                imc_gestacional=data.get('imc_gestacional'),
                semana_gestacion=data.get('semana_gestacion'),
                seleccion_multiple=data.get('clasificacion_peso', 'Sobrepeso'),
            )

            # Título 2: Peso de referencia
            sobrepeso_info = SobrePesoInfo.objects.create(
                base_info=gestante_info,
                imc_saludable=data.get('imc_saludable', 0.0),
                peso_pregestacional_saludable=data.get('peso_pregestacional_saludable', 0.0),

                # Título 3: Ganancia de peso
                gramos_semana=data.get('gramos_semana', 0.0),
                ganancia_1_trimestre=data.get('ganancia_1_trimestre', 0.0),
                ganancia_2_y_3_trimestre_gramos=data.get('ganancia_2_y_3_trimestre_gramos', 0.0),
                ganancia_2_y_3_trimestre_kg=data.get('ganancia_2_y_3_trimestre_kg', 0.0),
                peso_total_embarazo=data.get('peso_total_embarazo', 0.0),
                imc_semana_40=data.get('imc_semana_40', 0.0),

                # Título 4: % de peso pregestacional saludable (6 campos)
                ganancia_peso_embarazo=data.get('ganancia_peso_embarazo', 0.0),         # Campo 1
                ganancia_peso_clasificacion=data.get('ganancia_peso_clasificacion', ''), # Campo 2
                ganancia_primer_trimestre=data.get('ganancia_primer_trimestre', 0.0),    # Campo 3
                ganancia_2y3_trimestre_gsem=data.get('ganancia_2y3_trimestre_gsem', 0.0),# Campo 4
                peso_total_embarazo_titulo_4=data.get('peso_total_embarazo_titulo_4', 0.0), # Campo 5
                imc_semana_40_titulo_4=data.get('imc_semana_40_titulo_4', 0.0),          # Campo 6

                # Título 5: Evaluación de ganancia de peso
                ganancia_tipo=data.get('ganancia_tipo', 'g/sem'),
                gano=data.get('gano', 0.0),
                debio_ganar=data.get('debio_ganar', 0.0),

                # Título 6: Reprogramación
                peso_a_ganar=data.get('peso_a_ganar', 0.0),
                semanas_faltantes=data.get('semanas_faltantes', 0),
                gramos_por_semana=data.get('gramos_por_semana', 0.0),
                clasificacion_gramos=data.get('clasificacion_gramos', 'Adecuado'),

                # Título 7: Requerimiento de energía (5 campos)
                tasa_metabolica=data.get('tasa_metabolica', 0.0),              # Campo 1
                factor_actividad_fisica=data.get('factor_actividad_fisica', 1.4), # Campo 2
                requerimiento_energia_total=data.get('requerimiento_energia_total', 0.0), # Campo 3
                adicion_gestante=data.get('adicion_gestante', 500),            # Campo 4
                total_energia_adicion=data.get('total_energia_adicion', 0.0),  # Campo 5

                # Título 8: Aporte proteico
                metodo1_g_dia=data.get('metodo1_g_dia', 0.0),
                metodo1_kcal=data.get('metodo1_kcal', 0.0),
                metodo1_amdr=data.get('metodo1_amdr', 0.0),
                metodo2_g_dia=data.get('metodo2_g_dia', 0.0),
                metodo2_kcal=data.get('metodo2_kcal', 0.0),
                metodo2_amdr=data.get('metodo2_amdr', 0.0)
            )

            return Response({"message": "Datos de sobrepeso guardados correctamente"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, gestante_id):
        try:
            # Buscar la información de la gestante
            gestante_info = GestanteInfo.objects.get(id=gestante_id)
            sobrepeso_info = SobrePesoInfo.objects.get(base_info=gestante_info)

            # Crear la respuesta con toda la información relevante
            data = {
                # Título 1: Datos personales
                'gestante_info': {
                    'nombre': gestante_info.nombre,
                    'edad': gestante_info.edad,
                    'estatura': gestante_info.estatura,
                    'peso_actual': gestante_info.peso_actual,
                    'peso_pregestacional': gestante_info.peso_pregestacional,
                    'imc_pregestacional': gestante_info.imc_pregestacional,
                    'imc_gestacional': gestante_info.imc_gestacional,
                    'semana_gestacion': gestante_info.semana_gestacion,
                    'seleccion_multiple': gestante_info.seleccion_multiple
                },
                # Título 2: Peso de referencia
                'sobrepeso_info': {
                    'imc_saludable': sobrepeso_info.imc_saludable,
                    'peso_pregestacional_saludable': sobrepeso_info.peso_pregestacional_saludable,
                    
                    # Título 3: Ganancia de peso
                    'gramos_semana': sobrepeso_info.gramos_semana,
                    'ganancia_1_trimestre': sobrepeso_info.ganancia_1_trimestre,
                    'ganancia_2_y_3_trimestre_gramos': sobrepeso_info.ganancia_2_y_3_trimestre_gramos,
                    'ganancia_2_y_3_trimestre_kg': sobrepeso_info.ganancia_2_y_3_trimestre_kg,
                    'peso_total_embarazo': sobrepeso_info.peso_total_embarazo,
                    'imc_semana_40': sobrepeso_info.imc_semana_40,

                    # Título 4: % de peso pregestacional saludable (6 campos)
                    'ganancia_peso_embarazo': sobrepeso_info.ganancia_peso_embarazo,          # Campo 1
                    'ganancia_peso_clasificacion': sobrepeso_info.ganancia_peso_clasificacion, # Campo 2
                    'ganancia_primer_trimestre': sobrepeso_info.ganancia_primer_trimestre,     # Campo 3
                    'ganancia_2y3_trimestre_gsem': sobrepeso_info.ganancia_2y3_trimestre_gsem,# Campo 4
                    'peso_total_embarazo_titulo_4': sobrepeso_info.peso_total_embarazo_titulo_4, # Campo 5
                    'imc_semana_40_titulo_4': sobrepeso_info.imc_semana_40_titulo_4,           # Campo 6

                    # Título 5: Evaluación de ganancia de peso
                    'ganancia_tipo': sobrepeso_info.ganancia_tipo,
                    'gano': sobrepeso_info.gano,
                    'debio_ganar': sobrepeso_info.debio_ganar,

                    # Título 6: Reprogramación
                    'peso_a_ganar': sobrepeso_info.peso_a_ganar,
                    'semanas_faltantes': sobrepeso_info.semanas_faltantes,
                    'gramos_por_semana': sobrepeso_info.gramos_por_semana,
                    'clasificacion_gramos': sobrepeso_info.clasificacion_gramos,

                    # Título 7: Requerimiento de energía (5 campos)
                    'tasa_metabolica': sobrepeso_info.tasa_metabolica,              # Campo 1
                    'factor_actividad_fisica': sobrepeso_info.factor_actividad_fisica, # Campo 2
                    'requerimiento_energia_total': sobrepeso_info.requerimiento_energia_total, # Campo 3
                    'adicion_gestante': sobrepeso_info.adicion_gestante,            # Campo 4
                    'total_energia_adicion': sobrepeso_info.total_energia_adicion,  # Campo 5

                    # Título 8: Aporte proteico
                    'metodo1_g_dia': sobrepeso_info.metodo1_g_dia,
                    'metodo1_kcal': sobrepeso_info.metodo1_kcal,
                    'metodo1_amdr': sobrepeso_info.metodo1_amdr,
                    'metodo2_g_dia': sobrepeso_info.metodo2_g_dia,
                    'metodo2_kcal': sobrepeso_info.metodo2_kcal,
                    'metodo2_amdr': sobrepeso_info.metodo2_amdr
                }
            }

            return Response(data, status=status.HTTP_200_OK)

        except (GestanteInfo.DoesNotExist, SobrePesoInfo.DoesNotExist):
            return Response({"error": "Gestante o información de sobrepeso no encontrada"}, status=status.HTTP_404_NOT_FOUND)
