from django.shortcuts import render
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import *
from sqlite3 import OperationalError
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

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
formulario_filtro = """
        <form action="/filtro" method="POST">
          <input type="submit" value="Filtrar por accesibilidad">
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
                        #print(k.attrib);
                        idMuseo = k.find('[@nombre="ID-ENTIDAD"]').text
                        #print (idMuseo)
                    except AttributeError:
                        pass

                    try:
                        nombre = k.find('[@nombre="NOMBRE"]').text
                        #print (nombre)
                    except AttributeError:
                        pass

                    try:
                        descripcion = k.find('[@nombre="DESCRIPCION-ENTIDAD"]').text
                        #print (descripcion)
                    except AttributeError:
                        pass

                    try:
                        horario = k.find('[@nombre="HORARIO"]').text
                        #print (horario)
                    except AttributeError:
                        pass

                    try:
                        transporte = k.find('[@nombre="TRANSPORTE"]').text
                        #print (transporte)
                    except AttributeError:
                        pass

                    try:
                        url = k.find('[@nombre="CONTENT-URL"]').text
                        #print (url)
                    except AttributeError:
                        pass

                    try:
                        distrito = k.find('[@nombre="DISTRITO"]').text
                        #print (distrito)
                        #print("campo distrito")
                    except AttributeError:
                        pass

                    try:
                        email = k.find('[@nombre="EMAIL"]').text
                        #print (email)
                    except AttributeError:
                        pass

                    try:
                        accesibilidad = k.find('[@nombre="ACCESIBILIDAD"]').text
                        if accesibilidad == '0':
                            False;
                        else:
                            True;
                        #print(str(accesibilidad))
                    except AttributeError:
                        pass
        except AttributeError:
            continue

        museo = Museo(idMuseo = idMuseo, nombre = nombre,
                      descripcion = descripcion, horario = horario,
                      transporte = transporte,  accesibilidad = accesibilidad,
                      url = url, distrito = distrito, email = email)

        museo.save()
    return HttpResponse(formulario_carga)

@csrf_exempt
def pagina_principal(request):
    resp = "<h3>Museos de la ciudad de Madrid:</h3>"
    if request.method == 'GET':
        museos_comentados = Museo.objects.annotate(num_com=Count('comentario')).order_by('-num_com')[:5]

        for objeto in museos_comentados:
            resp += '<li><a href="/' + str(objeto.nombre) + '">' + objeto.nombre + '</a>'
            resp += "</ul>"
        return HttpResponse(resp + formulario_filtro)

@csrf_exempt
def filtro_accesibilidad(request):
    if request.method == 'POST':
        resp = "<h3>Museos de la ciudad de Madrid:</h3>"
        museos_accesibles = Museo.objects.filter(accesibilidad=1)[:5]
        for objeto in museos_accesibles:
            resp += '<li><a href="/' + str(objeto.nombre) + '">' + objeto.nombre + '</a>'
            resp += "</ul>"
        return HttpResponse(resp + formulario_volver)

def notOption(request, recurso):
    resp = "No contemplada esta opción."
    resp +="Lista opciones:"
    return HttpResponse(resp)
