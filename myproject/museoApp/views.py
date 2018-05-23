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
from django.contrib.auth.views import logout

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
formulario_seleccion = """
        <form action="" method="POST">
          <input type="submit" value="Seleccionar/Deseleccionar museo">
        </form>
        """
formulario_siguiente = """
        <form action="" method="POST">
          <input type="submit" value="Siguiente página">
        </form>
        """
formulario_comentario = """
        <form action="">
          <h3>PAGE:</h3>
          <input type="text" name="Comentario" value=""><br>
          <input type="submit" value="Enviar">
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
                        print(idMuseo)
                    except AttributeError:
                        pass
                    try:
                        nombre = k.find('[@nombre="NOMBRE"]').text
                        print(nombre)
                    except AttributeError:
                        pass
                    try:
                        descripcion = k.find('[@nombre="DESCRIPCION-ENTIDAD"]').text
                        print(descripcion)
                    except AttributeError:
                        pass
                    try:
                        horario = k.find('[@nombre="HORARIO"]').text
                        print(horario)
                    except AttributeError:
                        pass
                    try:
                        transporte = k.find('[@nombre="TRANSPORTE"]').text
                        print(transporte)
                    except AttributeError:
                        pass
                    try:
                        accesibilidad = k.find('[@nombre="ACCESIBILIDAD"]').text
                        print(accesibilidad)
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
                      url = url, direccion = direccion, barrio = barrio,
                      distrito = distrito, telefono = telefono, email = email)

        museo.save()

    return HttpResponse(formulario_carga)

def pagina_principal(request):

    if request.method == 'GET':
        if request.user.is_authenticated():
            sesion = 'Bienvenido: ' + request.user.username + '</br><a href="/logout">Logout</a>'
        else:
            sesion = '<li><a href="/login">Login</a>'
        museos_comentados = Museo.objects.annotate(num_com=Count('comentario')).filter(num_com__gte=1).order_by('-num_com')[:5]
        try:
            if museos_comentados[0].id:
                resp = "<h3>Museos de la ciudad de Madrid más comentados:</h3>"
                list = museos_comentados
        except IndexError:
            resp = "<h3>Museos de la ciudad de Madrid(no hay comentarios):</h3>"
            list = Museo.objects.all()


        for objeto in list:
            resp += '<li><a href="' + str(objeto.url) + '">' + objeto.nombre + ' en ' + objeto.direccion
            resp += '</a></br><a href="/museos/' + str(objeto.id) + '">' + "Más información" + '</a>'
            resp += "</ul>"
        return HttpResponse(sesion + resp +  formulario_acceso)


@csrf_exempt
def filtro_accesibilidad(request):
    if request.method == 'POST':
        resp = "<h1>Museos de la ciudad de Madrid accesibles:</h1>"
        museos_accesibles = Museo.objects.filter(accesibilidad=1)
        for objeto in museos_accesibles:
            resp += '<li><a href="/' + str(objeto.id) + '">' + objeto.nombre + '</a>'
            resp += "</ul>"
        return HttpResponse(resp + formulario_volver)

def museos(request):
    resp = "<h1>Todos los museos de la ciudad de Madrid:</h1>"
    museos_lista = Museo.objects.all()
    for objeto in museos_lista:
        resp += '<li><a href="/museos/' + str(objeto.id) + '">' + objeto.nombre + '</a></br>'
        resp += "</ul>"
    return HttpResponse(formulario_distrito + resp)

@csrf_exempt
def distrito(request):
    if request.method == 'POST':
        resp = "<h1>Distritos de la ciudad de Madrid:</h1>"
        lista_distritos = Museo.objects.values_list('distrito', flat=True).distinct()
        for objeto in lista_distritos:
            resp += '<li><a href="/distrito/' + objeto +  '">' + objeto + '</a></br>'
            resp += "</ul>"
    return HttpResponse(resp + formulario_volver)

def distrito_concreto(request, recurso):
    distrito_elegido = recurso
    if request.method == 'GET':
        resp = '<h1>Museos en ' + distrito_elegido + ': </h1>'
        museos_distritos = Museo.objects.filter(distrito = distrito_elegido)
        print(museos_distritos)
        for objeto in museos_distritos:
            resp += '<li><a href="/museos/' + str(objeto.id) + '">' + objeto.nombre + '</a></br>'
            resp += "</ul>"
    return HttpResponse(resp + formulario_volver)

@csrf_exempt
def museos_id(request,recurso):
    objeto = Museo.objects.get(id=recurso)
    comentarios = Comentario.objects.all()

    if objeto.accesibilidad == 0:
        acc = 'Mala'
    else:
        acc = 'Buena'

    resp = '<h1>MUSEO:</h1>' + " "'<h1>' + objeto.nombre + '</h1></br><h3>Descripción:</h3>' + objeto.descripcion +  '</br>'
    resp += '<h3>Horario:</h2>' + objeto.horario + '</br><h3>Transporte:</h3>' + objeto.transporte + '</br><h3>Accesibilidad:</h3>' + acc
    resp += '<h3>URL:</h3><a href="' + str(objeto.url) + '">' + objeto.url + '</a><h3>Dirección:</h3>' + objeto.direccion +'</br><h3>Barrio:</h3>' + objeto.barrio
    resp += '</br><h3>Distrito:</h3>' + objeto.distrito +'</br><h3>Teléfono:</h3>' + objeto.telefono + '</br><h3>Email:</h3>' + objeto.email
    resp += '<h3>Comentarios:</h3>'

    comentarios = Comentario.objects.filter(museo__nombre__contains = objeto.nombre)
    if str(comentarios) == '[]':
        com = "No hay comentarios hasta el momento en este museo."
        resp += com + "</ul>"
    else:
        for i in comentarios:
            com = i.comentario
            resp += com + '</br>'
        resp += "</ul>"

    if request.method =='GET':
        if request.user.is_authenticated():
            #formulario_comentario
            return HttpResponse(resp + formulario_seleccion)
        else:
            return HttpResponse(resp)

    if request.method =='POST':
        user_seleccion = request.user.username
        try:
            museo_usuario = Content_User.objects.get(usuario = user_seleccion, museo = objeto)
            museo_usuario.delete()
        except ObjectDoesNotExist:
            museo_usuario = Content_User(usuario = user_seleccion, museo = objeto)
            museo_usuario.save()
        return HttpResponse(resp + formulario_seleccion)

def mylogout(request):
    logout(request)
    return HttpResponseRedirect('/')

@csrf_exempt
def user(request, recurso):
    usuario = recurso.split('/')[0]
    museos_usuario = Content_User.objects.filter(usuario = recurso)
    try:
        long_recurso  = recurso.split('/')[1]
        root = ET.Element('Contenidos')
        child = ET.SubElement(root, 'atributo')
        for i in museos_usuario:
            subchild = ET.SubElement(child, "NOMBRE", str(i.museo.nombre))
        return HttpResponse(ET.tostring(root))
    except IndexError:
        resp = "Página de " + recurso + ":"
        num_museos = len(museos_usuario)
        if request.method =='GET':
            n_paginas = num_museos / 5
            if num_museos > 5:
                for objeto in museos_usuario[:5]:
                    resp += '<li><a href="' + str(objeto.museo.url) + '">' + objeto.museo.nombre + ' en ' + objeto.museo.direccion
                    resp += '</a></br><a href="/museos/' + str(objeto.museo.id) + '">' + "Más información" + '</a></br>'
                    resp += "</ul>"
                return HttpResponse(resp + formulario_siguiente)
            else:
                for objeto in museos_usuario:
                    resp += '<li><a href="' + str(objeto.museo.url) + '">' + objeto.museo.nombre + ' en ' + objeto.museo.direccion
                    resp += '</a></br><a href="/museos/' + str(objeto.museo.id) + '">' + "Más información" + '</a></br>'
                    resp += "</ul>"
                return HttpResponse(resp)
        if request.method =='POST':
            for objeto in museos_usuario[5:num_museos]:
                resp += '<li><a href="' + str(objeto.museo.url) + '">' + objeto.museo.nombre + ' en ' + objeto.museo.direccion
                resp += '</a></br><a href="/museos/' + str(objeto.museo.id) + '">' + "Más información" + '</a></br>'
                resp += "</ul>"
            return HttpResponse(resp)

def about(request):
    intro = "Página realizada por Cayetana Gómez Casado."
    funcionamiento = "Aquí tienes las diferentes urls disponibles que te ayudarán a su correcto funcionamiento:"
    resp = '<h1> Aplicación de museos de la ciudad de madrid </h1>'
    resp += '<h3>' + intro + '</br>' + funcionamiento + '</h3>'
    resp += '<li><a href="/cargar">' + 'Cargar base de datos.' + '</a></br>'
    resp += "</ul>"
    resp += '<li><a href="/">' + 'Página principal.' + '</a></br>'
    resp += "</ul>"
    resp += '<li><a href="/museos">' + 'Página con todos los museos que hay en la ciudad de Madrid.' + '</a></br>'
    resp += "</ul>"
    resp += '<li><a href="/museos/">' + 'Página de cada museo.' + '</a></br>'
    resp += "</ul>"
    return HttpResponse(resp)

def notOption(request, recurso):
    resp = "No contemplada esta opción.</br>"
    resp +="Quizás pueda ayudarte la siguiente página: </br>"
    resp += '<li><a href="/about">' + 'Página con la auditoría y el funcionamiento.' + '</a></br>'
    resp += "</ul>"
    return HttpResponse(resp)
