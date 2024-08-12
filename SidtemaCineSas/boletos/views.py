from django.shortcuts import render
from datetime import datetime

# Create your views here.
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .models import Pelicula, Funcion, Asiento, Boleto, PeliculaEstreno


def buscar_peliculas(request):
    fecha = request.GET.get('fecha')
    funciones = []

    if fecha:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()  
        funciones = Funcion.objects.filter(horario__date=fecha_obj)  

    return render(request, 'boletos/funciones_por_fecha.html', {
        'funciones': funciones,
        'fecha': fecha
    })

def lista_peliculas(request):
    estrenos = PeliculaEstreno.objects.all()
    peliculas = Pelicula.objects.all()
    request.session['boletos_seleccionados'] = []
    request.session.modified = True
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


from django.http import HttpResponse
def comprar_boleto(request, funcion_id, asiento_id):
    if 'boletos_seleccionados' not in request.session:
        request.session['boletos_seleccionados'] = []
    
    # Añadir el asiento a la lista de boletos seleccionados en la sesión
    if {'funcion_id': funcion_id, 'asiento_id': asiento_id} not in request.session['boletos_seleccionados']:
        request.session['boletos_seleccionados'].append({'funcion_id': funcion_id, 'asiento_id': asiento_id})
        request.session.modified = True
    
    return HttpResponse(status=204)


def confirmar_compra(request):
    boletos = []
    if 'boletos_seleccionados' in request.session:
        for item in request.session['boletos_seleccionados']:
            funcion = get_object_or_404(Funcion, id=item['funcion_id'])
            asiento = get_object_or_404(Asiento, id=item['asiento_id'])
            boleto, created = Boleto.objects.get_or_create(funcion=funcion, asiento=asiento)
            if created or not boleto.comprado:
                boleto.comprado = True
                boleto.save()
                boletos.append(boleto)
        request.session['boletos_seleccionados'] = []
        request.session.modified = True

    if boletos:
        return render(request, 'boletos/confirmacion.html', {'boletos': boletos})
    else:
        return redirect('lista_peliculas')




