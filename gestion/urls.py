from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_vista, name='login'),
    path('recepcion/', views.recepcion_vista, name='recepcion'),
    path('api/horarios/', views.obtener_horarios_ajax, name='api_horarios'),
    path('medico/', views.medico_vista, name='medico'),
    path('enfermeria/', views.enfermeria_vista, name='enfermeria'),
    path('administrador/', views.administrador_vista, name='administrador'),
    path('soporte/', views.soporte_vista, name='soporte'),
]