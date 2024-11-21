from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_usuario, name='login'),
    path('inicio/', views.inicio , name='inicio'),
    path('login/', views.login_usuario, name="login_usuario"),
    path('registro/', views.registrar_usuario, name="registrar_usuario"),
    path('escaneo/', views.escaneo, name='escaneo'),

    path('procesar_imagen/', views.procesar_imagen, name='procesar_imagen'),
    path('guardar_resultado/', views.guardar_resultado, name='guardar_resultado'),
    path('buscar_paciente/', views.buscar_paciente, name='buscar_paciente'),

    path('registrar_paciente/', views.registrar_paciente, name='registrar_paciente'),
    path('buscar_paciente/', views.buscar_paciente, name='buscar_paciente'),


    path('historial/', views.historial, name='historial'),  # URL para ver el historial
    path('eliminar_historial/<int:id>/', views.eliminar_historial, name='eliminar_historial'),

    path('resultado/', views.resultado, name='resultado'),
    path('logout/', views.logout_usuario, name='logout'),

  
]