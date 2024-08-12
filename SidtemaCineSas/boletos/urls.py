from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_peliculas, name='lista_peliculas'),
    path('buscar/', views.buscar_peliculas, name='buscar_peliculas'),  # Aquí el cambio
    path('confirmar/', views.confirmar_compra, name='confirmar_compra'),  # Aquí el cambio
    path('pelicula/<int:pelicula_id>/', views.detalles_pelicula, name='detalles_pelicula'),
    path('funcion/<int:funcion_id>/', views.seleccionar_asiento, name='seleccionar_asiento'),
    path('comprar/<int:funcion_id>/<int:asiento_id>/', views.comprar_boleto, name='comprar_boleto'),
]
