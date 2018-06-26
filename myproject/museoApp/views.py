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
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
import json

formulario_carga = """
        <form action="/">
          <h3>CARGAR DATOS:</h3>
          <input type="submit" value="Cargar museos">
        </form>
        """
formulario_comentario = """
        <form action="/comentario_nuevo" method="POST">
          <h3>Comentar:</h3>
          <input type="hidden" name="museo" value="{}">
          <textarea name="Comentario" cols="40" rows="5"></textarea><br>
          <input type="submit" value="Enviar">
        </form>
        """
formulario_pagina = """
        <form action="" method="POST">
          <input type="hidden" name="n" value="{}">
          <input type="submit" value="{}">
        </form>
        """

FUENTE_CSS_DEFAULT = '62.5'
COLOR_CSS_DEFAULT = 'white'

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
                            "Mala";
                        else:
                            "Buena";
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

def style(request):
    print('Estoy en style')
    return HttpResponse(render(request, 'style.css'), content_type="text/css")

def notOption():
    resp = "No contemplada esta opción.</br>"
    resp +="Quizás pueda ayudarte la siguiente página: </br>"
    resp += '<li><a href="/about">' + 'Página con la auditoría y el funcionamiento.' + '</a></br>'
    resp += "</ul>"
    return (resp)

def get_museos_comentados(lista):
    resp = ""
    for objeto in lista:
        resp += '<li><a href="' + str(objeto.url) + '">' + objeto.nombre + '</a></br>'
        resp += 'Dirección: ' + objeto.direccion + ', ' + objeto.barrio + ', ' + objeto.distrito + '.'
        resp += '</br><a href="/museos/' + str(objeto.id) + '">' + "Más información" + '</a>'
        resp += "</ul>"
    return (resp)

def get_museos_seleccionados(lista):
    resp = ""
    for objeto in lista:
        resp += '<li><a href="' + str(objeto.museo.url) + '">' + objeto.museo.nombre + '</a></br>'
        resp += 'Dirección: ' + objeto.museo.direccion + ', ' + objeto.museo.barrio + ', ' + objeto.museo.distrito + '.'
        resp += '</br><a href="/museos/' + str(objeto.museo.id) + '">' + "Más información" + '</a>'
        resp += "</ul>"
    return (resp)

def pagina_principal(request):

    if request.method == 'GET':
        museos_seleccionados = Content_User.objects.annotate(num_sel=Count('museo')).filter(num_sel__gte=1).order_by('-num_sel')[:5]
        try:
            if museos_seleccionados[0].id:
                resp = "<h3>Museos más seleccionados:</h3>"
                resp += get_museos_seleccionados(museos_seleccionados)
        except IndexError:
            museos_comentados = Museo.objects.annotate(num_com=Count('comentario')).filter(num_com__gte=1).order_by('-num_com')[:5]
            try:
                if museos_comentados[0].id:
                    resp = "<h3>Museos más comentados:</h3>"
                    resp += get_museos_comentados(museos_comentados)
            except IndexError:
                resp = "<h3>No hay museos seleccionados ni comentados en la ciudad de Madrid hasta el momento.</h3>"

        lista_usuarios = User.objects.all()

        context = {'usuario': request.user.username, 'autentificado': request.user.is_authenticated(), 'respuesta': resp, 'lista_usuarios': lista_usuarios}
        return render(request, 'principal.html', context)


@csrf_exempt
def filtro_accesibilidad(request):
    if request.method == 'POST':
        resp = "<h3>Museos accesibles:</h3>"
        museos_accesibles = Museo.objects.filter(accesibilidad=1)
        acceso= True
        for objeto in museos_accesibles:
            resp += '<li><a href="/museos/' + str(objeto.id) + '">' + objeto.nombre + '</a>'
            resp += "</ul>"
        lista_usuarios = User.objects.all()
        context = {'usuario': request.user.username, 'autentificado': request.user.is_authenticated(), 'filtro_acc': resp, 'acceso': acceso, 'lista_usuarios': lista_usuarios}
        return render(request, 'principal.html', context)

def museos(request):
    resp = "<h3>Todos los museos:</h3>"
    museos_lista = Museo.objects.all()
    for objeto in museos_lista:
        resp += '<li><a href="/museos/' + str(objeto.id) + '">' + objeto.nombre + '</a></br>'
        resp += "</ul>"
    context = {'usuario': request.user.username, 'autentificado': request.user.is_authenticated(), 'respuesta': resp}
    resp = None
    return render(request, 'museos.html', context)

@csrf_exempt
def distrito(request):
    if request.method == 'POST':
        dist = True
        resp = "<h3>Distritos posibles:</h3>"
        lista_distritos = Museo.objects.values_list('distrito', flat=True).distinct()
        for objeto in lista_distritos:
            resp += '<li><a href="/distrito/' + objeto +  '">' + objeto + '</a></br>'
            resp += "</ul>"
    context = {'usuario': request.user.username, 'autentificado': request.user.is_authenticated(), 'filtro_dist': resp, 'dist': dist}
    resp = dist = None
    return render(request, 'museos.html', context)

def distrito_concreto(request, recurso):
    distrito_elegido = recurso
    if request.method == 'GET':
        dist = False
        concreto = True
        resp = '<h3>Museos en ' + distrito_elegido + ': </h3>'
        museos_distritos = Museo.objects.filter(distrito = distrito_elegido)
        for objeto in museos_distritos:
            resp += '<li><a href="/museos/' + str(objeto.id) + '">' + objeto.nombre + '</a></br>'
            resp += 'Dirección: ' + objeto.direccion + ', ' + objeto.barrio + '.'
            resp += "</ul>"
    context = {'usuario': request.user.username, 'autentificado': request.user.is_authenticated(), 'distrito_concreto': resp, 'dist': dist, 'concreto': concreto}
    resp = dist = concreto = None
    return render(request, 'museos.html', context)

@csrf_exempt
def comentar(request):
    museo = request.POST['museo']
    comentario  = request.POST['Comentario']
    museo = Museo.objects.get(nombre=museo)
    museo_comentado = Comentario(museo = museo, comentario = comentario)
    museo_comentado.save()
    return HttpResponseRedirect('/')

@csrf_exempt
def museos_id(request,recurso):
    objeto = Museo.objects.get(id=recurso)
    comentarios = Comentario.objects.all()

    if objeto.accesibilidad == 0:
        acc = 'Mala'
    else:
        acc = 'Buena'

    resp = '<h1>' + objeto.nombre + '</h1></br><h4>Descripción:</h4>' + objeto.descripcion +  '</br>'
    resp += '<h4>Horario:</h4>' + objeto.horario + '</br><h4>Transporte:</h4>' + objeto.transporte + '</br><h4>Accesibilidad:</h4>' + acc
    resp += '<h4>URL:</h4><a href="' + str(objeto.url) + '">' + objeto.url + '</a><h4>Dirección:</h4>' + objeto.direccion +'</br><h4>Barrio:</h4>' + objeto.barrio
    resp += '</br><h4>Distrito:</h4>' + objeto.distrito +'</br><h4>Teléfono:</h4>' + objeto.telefono + '</br><h4>Email:</h4>' + objeto.email
    resp += '<h4>Comentarios:</h4>'

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
            sel = True
            coment = True
            context = {'usuario': request.user.username, 'autentificado': request.user.is_authenticated(), 'respuesta': resp, 'seleccion': sel, 'comentar': coment, 'form': formulario_comentario.format(objeto.nombre)}
        else:
            sel = False
            coment = False
            context = {'usuario': request.user.username, 'autentificado': request.user.is_authenticated(), 'respuesta': resp, 'seleccion': sel, 'comentar': coment}

    if request.method =='POST':
        user_seleccion = request.user
        try:
            museo_usuario = Content_User.objects.get(usuario = user_seleccion, museo = objeto)
            museo_usuario.delete()
        except ObjectDoesNotExist:
            museo_usuario = Content_User(usuario = user_seleccion, museo = objeto)
            museo_usuario.save()

        sel = True
        coment = False
        context = {'usuario': request.user.username, 'autentificado': request.user.is_authenticated(), 'respuesta': resp, 'seleccion': sel, 'comentar': coment}

    return render(request, 'museo_id.html', context)

def mylogout(request):
    logout(request)
    return HttpResponseRedirect('/')

@csrf_exempt
def mylogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        #opcion registro de usuarios
        return HttpResponseRedirect('/')

def elementos_json(elementos, museo):
    elemento = {}
    elemento['idMuseo'] = museo.museo.idMuseo
    elemento['nombre'] = museo.museo.nombre
    elemento['descripcion'] = museo.museo.descripcion
    elemento['horario'] = museo.museo.horario
    elemento['transporte'] = museo.museo.transporte
    elemento['accesibilidad'] = museo.museo.accesibilidad
    elemento['url'] = museo.museo.url
    elemento['direccion'] = museo.museo.direccion
    elemento['barrio'] = museo.museo.barrio
    elemento['distrito'] = museo.museo.distrito
    elemento['telefono'] = museo.museo.telefono
    elemento['email'] = museo.museo.email
    elementos.append(elemento)

def json_cod(museos):
    diccionario = {}
    diccionario['museos'] = []
    for i in museos:
        print(i)
        elementos_json(diccionario['museos'], i)
    data = json.dumps(diccionario, indent=4)
    return data

def insertar_atributo_xml(child, atributo, valor):
    atrib = ET.SubElement(child, 'atributo', {'nombre': atributo})
    atrib.text = valor

def insertar_museo_xml(child, museo):
    insertar_atributo_xml(child, "ID-ENTIDAD", str(museo.idMuseo))
    insertar_atributo_xml(child, "NOMBRE", str(museo.nombre))
    insertar_atributo_xml(child, "DESCRIPCION-ENTIDAD", str(museo.descripcion))
    insertar_atributo_xml(child, "HORARIO", str(museo.horario))
    insertar_atributo_xml(child, "TRANSPORTE", str(museo.transporte))
    insertar_atributo_xml(child, "ACCESIBILIDAD", str(museo.accesibilidad))
    insertar_atributo_xml(child, "CONTENT-URL", str(museo.url))
    insertar_atributo_xml(child, "NOMBRE-VIA", str(museo.direccion))
    insertar_atributo_xml(child, "BARRIO", str(museo.barrio))
    insertar_atributo_xml(child, "DISTRITO", str(museo.distrito))
    insertar_atributo_xml(child, "TELEFONO", str(museo.telefono))
    insertar_atributo_xml(child, "EMAIL", str(museo.email))

def xml_cod(museos):
    root = ET.Element('Contenidos')
    for i in museos:
        child = ET.SubElement(root, 'museo')
        insertar_museo_xml(child, i.museo)
    return ET.tostring(root)

@csrf_exempt
def estiloUser(request):
    return HttpResponseRedirect('/')

@csrf_exempt
def tituloUser(request):
    titulo  = request.POST['Título']
    usuario = request.user
    try:
        user_titulo = Configuracion.objects.get(usuario=usuario)
        user_titulo.delete()
    except ObjectDoesNotExist:
        pass;
    user_titulo = Configuracion(titulo = titulo, usuario=usuario)
    user_titulo.save()
    return HttpResponseRedirect('/')

def get_configuracion(usuario):
    estilo = Configuracion.objects.filter(usuario__username__contains=usuario)
    print(estilo)
    if str(estilo) != '[]':
        for i in estilo:
            titulo = i.titulo
            if str(titulo) == '':
                titulo = '<h3>Página de ' + usuario + '</h3>'
            else:
                titulo = '<h3>' + str(titulo) + '</h3>'
            fuente = i.fuente
            if str(fuente) == '':
                fuente = FUENTE_CSS_DEFAULT
            color = i.color
            if str(color) == '':
                color = COLOR_CSS_DEFAULT
    else:
        titulo = '<h3>Página de ' + usuario + '</h3>'
        fuente = FUENTE_CSS_DEFAULT
        color = COLOR_CSS_DEFAULT
    print(titulo + ' ' + fuente + ' ' + color)
    return(titulo,fuente, color)
    #return HttpResponse(render(request, 'style.css', context), content_type="text/css")

@csrf_exempt
def user(request, recurso):
    usuario = recurso.split('/')[0]
    print('primer usuario:' + usuario)
    try:
        usuario_encontrado = User.objects.get(username=usuario)
        print(usuario_encontrado)
        museos_usuario = Content_User.objects.filter(usuario__username__contains = usuario)
        titulo,fuente,color = get_configuracion(usuario)
        acceso = False
        if request.user.is_authenticated() and str(request.user.username) == str(usuario):
            acceso = True
        try:
            long_recurso  = recurso.split('/')[1]
            if str(long_recurso) == 'json':
                json = json_cod(museos_usuario)
                return HttpResponse(json, content_type="application/json")
            if str(long_recurso) == 'xml':
                xml = xml_cod(museos_usuario)
                return HttpResponse(xml, content_type="text/xml")
        except IndexError:

            num_museos = len(museos_usuario)
            n_paginas = int((num_museos / 5) + 1 )
            ans = "</br> Páginas disponibles:</br>"
            for i in range(1,n_paginas+1):
                 ans += formulario_pagina.format(i,i)

            resp = ""
            if request.method =='GET':
                for objeto in museos_usuario[:5]:
                    resp += '<li><a href="' + str(objeto.museo.url) + '">' + objeto.museo.nombre + ' en ' + objeto.museo.direccion
                    resp += '</a></br><a href="/museos/' + str(objeto.museo.id) + '">' + "Más información" + '</a> (' + str(objeto.fecha) + ')'
                    resp += "</ul>"
                context = {'usuario': request.user.username, 'autentificado': request.user.is_authenticated(), 'titulo': titulo, 'respuesta': resp, 'ans': ans, 'acceso': acceso, 'nombre': usuario}

            if request.method =='POST':
                n = int(request.POST['n'])
                if n*5 > num_museos:
                     fin = num_museos
                else:
                     fin = n*5
                for objeto in museos_usuario[(n-1)*5:n*5]:
                    resp += '<li><a href="' + str(objeto.museo.url) + '">' + objeto.museo.nombre + ' en ' + objeto.museo.direccion
                    resp += '</a></br><a href="/museos/' + str(objeto.museo.id) + '">' + "Más información" + '</a> (' + str(objeto.fecha) + ')'
                    resp += "</ul>"
                context = {'usuario': request.user.username, 'autentificado': request.user.is_authenticated(), 'titulo': titulo, 'respuesta': resp, 'ans': ans, 'acceso': acceso, 'nombre': usuario}

            return render(request, 'user.html', context)

            #if request.user.is_authenticated() and str(request.user.username) == str(usuario):
            #    print("Aquí tengo las configuraciones en la página de usuario(CSS)")
    except ObjectDoesNotExist:
        error = notOption()
        return HttpResponse(error)


def about(request):
    intro = "Página realizada por Cayetana Gómez Casado."
    funcionamiento = "Aquí tienes las diferentes urls disponibles que te ayudarán a su correcto funcionamiento:"
    context = {'usuario': request.user.username, 'autentificado': request.user.is_authenticated(), 'intro': intro, 'funcionamiento': funcionamiento}
    return render(request, 'about.html', context)
