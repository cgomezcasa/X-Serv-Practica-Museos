from django.shortcuts import render
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import *
from sqlite3 import OperationalError
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist

formulario_carga = """
        <form action="/">
          <h3>CARGAR DATOS:</h3>
          <input type="submit" value="Cargar museos">
        </form>
        """
formulario_volver = """
        <form action="/">
          <input type="submit" value="Página principal">
        </form>
        """
formulario_acceso = """
        <form action="/acceso" method="POST">
          <input type="submit" value="Filtrar por accesibilidad">
        </form>
        """
formulario_distrito = """
        <form action="/distrito" method="POST">
          <input type="submit" value="Filtrar por distrito">
        </form>
        """

def xmlParser(request):
    print("Estoy en parser")
    xml_Url = "https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full"
    page = urlopen(xml_Url)
    tree = ET.parse(page)
    root = tree.getroot()

    for i in root.iter('contenido'):
        try:
            for j in i.iter('atributos'):

                for k in j.iter('atributo'):
                    try:
                        idMuseo = k.find('[@nombre="ID-ENTIDAD"]').text
                    except AttributeError:
                        pass
                    try:
                        nombre = k.find('[@nombre="NOMBRE"]').text
                    except AttributeError:
                        pass
                    try:
                        descripcion = k.find('[@nombre="DESCRIPCION-ENTIDAD"]').text
                    except AttributeError:
                        pass
                    try:
                        horario = k.find('[@nombre="HORARIO"]').text
                    except AttributeError:
                        pass
                    try:
                        transporte = k.find('[@nombre="TRANSPORTE"]').text
                    except AttributeError:
                        pass
                    try:
                        accesibilidad = k.find('[@nombre="ACCESIBILIDAD"]').text
                        if accesibilidad == '0':
                            False;
                        else:
                            True;
                    except AttributeError:
                        pass
                    try:
                        url = k.find('[@nombre="CONTENT-URL"]').text
                    except AttributeError:
                        pass
                    try:
                        direccion = k.find('[@nombre="NOMBRE-VIA"]').text
                    except AttributeError:
                        pass
                    try:
                        barrio = k.find('[@nombre="BARRIO"]').text
                    except AttributeError:
                        pass
                    try:
                        distrito = k.find('[@nombre="DISTRITO"]').text
                    except AttributeError:
                        pass
                    try:
                        telefono = k.find('[@nombre="TELEFONO"]').text
                    except AttributeError:
                        pass
                    try:
                        email = k.find('[@nombre="EMAIL"]').text
                    except AttributeError:
                        pass
        except AttributeError:
            continue

        museo = Museo(idMuseo = idMuseo, nombre = nombre,
                      descripcion = descripcion, horario = horario,
                      transporte = transporte,  accesibilidad = accesibilidad,
                      url = url, direccion=direccion, barrio=barrio,
                      distrito = distrito, telefono=telefono, email = email)

        museo.save()
    return HttpResponse(formulario_carga)

def pagina_principal(request):

    if request.method == 'GET':
        museos_comentados = Museo.objects.annotate(num_com=Count('comentario')).filter(num_com__gte=1).order_by('-num_com')[:5]
        try:
            if museos_comentados[0].id:
                resp = "<h3>Museos de la ciudad de Madrid más comentados:</h3>"
                list = museos_comentados
        except IndexError:
            resp = "<h3>Museos de la ciudad de Madrid(no hay comentarios):</h3>"
            list = Museo.objects.all()


        for objeto in list:
            resp += '<li><a href="' + str(objeto.url) + '">' + objeto.nombre + '</a></br><a href="/museo/' + str(objeto.id) + '">' + "Más información" + '</a>'
            resp += "</ul>"
            #tambien hay que añadir la direccion(objeto.direccion despues de objeto.nombre)
        return HttpResponse(resp +  formulario_acceso)

@csrf_exempt
def filtro_accesibilidad(request):
    if request.method == 'POST':
        resp = "<h3>Museos de la ciudad de Madrid accesibles:</h3>"
        museos_accesibles = Museo.objects.filter(accesibilidad=1)
        for objeto in museos_accesibles:
            resp += '<li><a href="/' + str(objeto.id) + '">' + objeto.nombre + '</a>'
            resp += "</ul>"
        return HttpResponse(resp + formulario_volver)

def museos(request):
    resp = "<h3>Todos los museos de la ciudad de Madrid:</h3>"
    museos_lista = Museo.objects.all()
    for objeto in museos_lista:
        resp += '<li><a href="/museo/' + str(objeto.id) + '">' + objeto.nombre + '</a></br>'
        resp += "</ul>"
    return HttpResponse(formulario_distrito + resp)

@csrf_exempt
def filtro_distrito(request):
    if request.method == 'POST':
        resp = "<h3>Museos de la ciudad de Madrid diferenciados por distritos:</h3>"
        museos_distrito = set(Museo.objects.filter(distrito=new))
        print(museos_distrito)
        for objeto in museos_distrito:
            resp += objeto

    return HttpResponse(resp + formulario_volver)

def museos_id(request,recurso):
    objeto = Museo.objects.get(id=recurso)
    comentarios = Comentario.objects.all()

    if objeto.accesibilidad == 0:
        acc = 'Mala'
    else:
        acc = 'Buena'

    resp = '<h1>MUSEO:</h1>' + " "'<h1>' + objeto.nombre + '</h1></br><h3>Descripción:</h3></br>' + objeto.descripcion +  '</br>'
    resp += '<h3>Horario:</h2>' + objeto.horario + '</br><h3>Transporte:</h3>' + objeto.transporte + '</br><h3>Accesibilidad:</h3>' + acc
    resp += '<h3>URL:</h3>' + objeto.url + '</br><h3>Distrito:</h3>' + objeto.distrito + '</br><h3>Email:</h3>' + objeto.email
    resp += '<h3>Comentarios:</h3>'
        #faltan direccion, barrio y telefono
    comentarios = Comentario.objects.filter(museo__nombre__contains = objeto.nombre)
    print(comentarios)
    if str(comentarios) == '[]':
        com = "No hay comentarios hasta el momento en este museo."
        resp += com + "</ul>"
    else:
        print("estoy antes del for")
        for i in comentarios:
            print("estoy dentro del for")
            print("i:" + str(i))
            com = i.comentario
            resp += com + '</br>'
        resp += "</ul>"
    return HttpResponse(resp)

def notOption(request, recurso):
    resp = "No contemplada esta opción."
    resp +="Lista opciones:"
    return HttpResponse(resp)
