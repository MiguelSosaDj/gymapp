from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from usuarios.views import (
    NinoSanoView, 
    NinoInfoView, 
    HomeDataView, 
    PersonasView, 
    AlumnoViewSet, 
    EntrenamientoViewSet, 
    LoginView, 
    SaveNinoInfo, 
    SaveLactanteInfo, 
    SaveGestanteInfo, 
    UserInfoView, 
    ListUsuariosView,
    LactanteView, GestanteView, SobrePesoView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'alumnos', AlumnoViewSet, basename='alumnos')
router.register(r'entrenamientos', EntrenamientoViewSet, basename='entrenamientos')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('api/', include(router.urls)),
    path('api/save-nino-info/', SaveNinoInfo.as_view(), name='save_nino_info'),
    path('api/save-lactante-info/', SaveLactanteInfo.as_view(), name='save_lactante_info'),
    path('api/save-gestante-info/', SaveGestanteInfo.as_view(), name='save_gestante_info'),
    path('api/user-info/', UserInfoView.as_view(), name='user_info'),
    path('api/usuarios/', ListUsuariosView.as_view(), name='list_usuarios'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/home-data/', HomeDataView.as_view(), name='home-data'),
    path('api/personas/', PersonasView.as_view(), name='personas'),
    path('api/nino-info/<int:nino_id>/', NinoInfoView.as_view(), name='nino_info'),
    path('api/nino-sano/', NinoSanoView.as_view(), name='nino_sano'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('lactante/', LactanteView.as_view(), name='lactante_info'),
    path('lactante/<int:lactante_id>/', LactanteView.as_view(), name='get_lactante_info'),
    path('gestante/<int:gestante_id>/', GestanteView.as_view(), name='gestante_info'),
    path('gestante/', GestanteView.as_view(), name='gestante_create'),
    path('sobrepeso/<int:sobrepeso_id>/', SobrePesoView.as_view(), name='sobrepeso_info'),
    path('sobrepeso/', SobrePesoView.as_view(), name='sobrepeso_create'),

]
