from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Pelicula, Funcion, Asiento, Boleto, PeliculaEstreno

admin.site.register(Pelicula)
admin.site.register(Funcion)
admin.site.register(Asiento)
admin.site.register(Boleto)
admin.site.register(PeliculaEstreno)
