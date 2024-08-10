from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Pelicula, Funcion, Asiento, Boleto, PeliculaEstreno

def lista_peliculas(request):
    estrenos = PeliculaEstreno.objects.all()
    peliculas = Pelicula.objects.all()
    return render(request, 'boletos/lista_peliculas.html', {'peliculas': peliculas, 'estrenos':estrenos})

def detalles_pelicula(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)
    funciones = Funcion.objects.filter(pelicula=pelicula)
    return render(request, 'boletos/detalles_pelicula.html', {'pelicula': pelicula, 'funciones': funciones})

def seleccionar_asiento(request, funcion_id):
    funcion = get_object_or_404(Funcion, id=funcion_id)
    asientos = Asiento.objects.all()
    boletos = Boleto.objects.filter(funcion=funcion)
    asientos_ocupados = [boleto.asiento.id for boleto in boletos if boleto.comprado]
    return render(request, 'boletos/seleccionar_asiento.html', {'funcion': funcion, 'asientos': asientos, 'asientos_ocupados': asientos_ocupados})

def comprar_boleto(request, funcion_id, asiento_id):
    funcion = get_object_or_404(Funcion, id=funcion_id)
    asiento = get_object_or_404(Asiento, id=asiento_id)
    boleto, created = Boleto.objects.get_or_create(funcion=funcion, asiento=asiento)
    if created or not boleto.comprado:
        boleto.comprado = True
        boleto.save()
    return render(request, 'boletos/confirmacion.html', {'boleto': boleto})
