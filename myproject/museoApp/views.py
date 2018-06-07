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
from django.contrib.auth.models import User
import json

formulario_carga = """
        <form action="/">
          <h3>CARGAR DATOS:</h3>
          <input type="submit" value="Cargar museos">
        </form>
        """
# formulario_volver = """
#         <form action="/">
#           <input type="submit" value="Página principal">
#         </form>
#         """
# formulario_distrito = """
#         <form action="/distrito" method="POST">
#           <input type="submit" value="Filtrar por distrito">
#         </form>
#         """
# formulario_seleccion = """
#         <form action="" method="POST">
#           <input type="submit" value="Seleccionar/Deseleccionar museo">
#         </form>
#         """
# formulario_siguiente = """
#         <form action="" method="POST">
#           <input type="submit" value="Siguiente página">
#         </form>
#         """
formulario_comentario = """
        <form action="/comentario_nuevo" method="POST">
          <h3>Comentar:</h3>
          <input type="hidden" name="museo" value="{}">
          <textarea name="Comentario" cols="40" rows="5"></textarea><br>
          <input type="submit" value="Enviar">
        </form>
        """
formulario_titulo = """
        <form action="/titulo_nuevo" method="POST">
          <h3>Titulo:</h3>
          <textarea name="Título" cols="30" rows="2"></textarea><br>
          <input type="submit" value="Enviar">
        </form>
        """
# formulario_acceso = """
#         <form action="/acceso" method="POST">
#         <input type="submit" value="Filtrar por accesibilidad">
#         </form>
#         """
formulario_pagina = """
        <form action="" method="POST">
          <input type="hidden" name="n" value="{}">
          <input type="submit" value="\n">
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
        if request.user.is_authenticated():
            sesion = 'Bienvenido: ' + request.user.username + '</br><a href="/logout">Logout</a>'
        else:
            sesion = '<li><a href="/login">Login</a>'

        museos_seleccionados = Content_User.objects.annotate(num_sel=Count('museo')).filter(num_sel__gte=1).order_by('-num_sel')[:5]
        try:
            if museos_seleccionados[0].id:
                resp = "<h3>Museos de la ciudad de Madrid más seleccionados:</h3>"
                resp += get_museos_seleccionados(museos_seleccionados)
        except IndexError:
            museos_comentados = Museo.objects.annotate(num_com=Count('comentario')).filter(num_com__gte=1).order_by('-num_com')[:5]
            try:
                if museos_comentados[0].id:
                    resp = "<h3>Museos de la ciudad de Madrid más comentados:</h3>"
                    resp += get_museos_comentados(museos_comentados)

            except IndexError:
                resp = "<h3>No hay museos seleccionados ni comentados en la ciudad de Madrid hasta el momento.</h3>"

        lista_usuarios = User.objects.all()

        context = {'respuesta': resp, 'lista_usuarios': lista_usuarios}
        return render(request, 'principal.html', context)
        #return HttpResponse(sesion + resp +  formulario_acceso + usuarios)


@csrf_exempt
def filtro_accesibilidad(request):
    if request.method == 'POST':
        resp = "<h3>Museos de Madrid accesibles:</h3>"
        museos_accesibles = Museo.objects.filter(accesibilidad=1)
        acceso= True
        for objeto in museos_accesibles:
            resp += '<li><a href="/museos/' + str(objeto.id) + '">' + objeto.nombre + '</a>'
            resp += "</ul>"
        lista_usuarios = User.objects.all()
        context = {'filtro_acc': resp, 'acceso': acceso, 'lista_usuarios': lista_usuarios}
        return render(request, 'principal.html', context)
        #return HttpResponse(resp + formulario_volver)

def museos(request):
    resp = "<h3>Todos los museos de la ciudad de Madrid:</h3>"
    museos_lista = Museo.objects.all()
    for objeto in museos_lista:
        resp += '<li><a href="/museos/' + str(objeto.id) + '">' + objeto.nombre + '</a></br>'
        resp += "</ul>"
    context = {'respuesta': resp}
    resp = None
    return render(request, 'museos.html', context)
    #return HttpResponse(formulario_distrito + resp)

@csrf_exempt
def distrito(request):
    if request.method == 'POST':
        dist = True
        resp = "<h3>Distritos de la ciudad de Madrid:</h3>"
        lista_distritos = Museo.objects.values_list('distrito', flat=True).distinct()
        for objeto in lista_distritos:
            resp += '<li><a href="/distrito/' + objeto +  '">' + objeto + '</a></br>'
            resp += "</ul>"
    context = {'filtro_dist': resp, 'dist': dist}
    resp = dist = None
    return render(request, 'museos.html', context)
    #return HttpResponse(resp + formulario_volver)

def distrito_concreto(request, recurso):
    distrito_elegido = recurso
    if request.method == 'GET':
        dist = False
        concreto = True
        resp = '<h3>Museos en ' + distrito_elegido + ': </h3>'
        museos_distritos = Museo.objects.filter(distrito = distrito_elegido)
        print(museos_distritos)
        for objeto in museos_distritos:
            resp += '<li><a href="/museos/' + str(objeto.id) + '">' + objeto.nombre + '</a></br>'
            resp += 'Dirección: ' + objeto.direccion + ', ' + objeto.barrio + '.'
            resp += "</ul>"
    context = {'distrito_concreto': resp, 'dist': dist, 'concreto': concreto}
    resp = dist = concreto = None
    return render(request, 'museos.html', context)
    #return HttpResponse(resp + formulario_volver)

@csrf_exempt
def comentar(request):
    museo = request.POST['museo']
    comentario  = request.POST['Comentario']
    museo = Museo.objects.get(nombre=museo)
    museo_comentado = Comentario(museo = museo, comentario = comentario)
    museo_comentado.save()
    return HttpResponseRedirect('/museos')

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
            context = {'respuesta': resp, 'seleccion': sel, 'comentar': coment, 'form': formulario_comentario.format(objeto.nombre)}
            #return HttpResponse(resp + formulario_seleccion + formulario_comentario.format(objeto.nombre))
        else:
            sel = False
            coment = False
            context = {'respuesta': resp, 'seleccion': sel, 'comentar': coment}
            #return HttpResponse(resp)

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
        context = {'respuesta': resp, 'seleccion': sel, 'comentar': coment}
        #return HttpResponse(resp + formulario_seleccion)


    return render(request, 'museo_id.html', context)

def mylogout(request):
    logout(request)
    return HttpResponseRedirect('/')

@csrf_exempt
def mylogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/' + str(user))
    else:
        #opcion registro de usuarios
        return HttpResponseRedirect('/')

def user_json(request, recurso):
    usuario = recurso.split('/')[0]
    print(str(usuario))
    museos_usuario = Content_User.objects.filter(usuario__username__contains = usuario)
    #aquí meto el template de json con el usuario y sus museos
    return HttpResponseRedirect('/')

def user_xml(request, recurso):
    usuario = recurso.split('/')[0]
    museos_usuario = Content_User.objects.filter(usuario__username__contains = usuario)
    #aquí meto el template de xml con el usuario y sus museos
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

def get_titulo(usuario):
    titulo = Configuracion.objects.filter(usuario__username__contains=usuario)
    for i in titulo:
        tituloUsuario = i.titulo
    print(str(tituloUsuario))
    if str(tituloUsuario) != '[]':
        titulo = '<h3>' + str(tituloUsuario) + '</h3>'
        tituloUsuario = None
    else:
        if request.user.is_authenticated() and str(request.user.username) == str(usuario):
            titulo = formulario_titulo
        else:
            titulo = '<h3>Página de ' + usuario + '</h3>'
    return(titulo)

@csrf_exempt
def user(request, recurso):
    usuario = recurso.split('/')[0]
    try:
        usuario_encontrado = User.objects.get(username=usuario)
        museos_usuario = Content_User.objects.filter(usuario__username__contains = usuario)
        xmlUser = '</br>'"Descargar fichero, "'<a href="/xml/' + str(usuario) + '">' + "xml"'</a>'
        titulo = get_titulo(usuario)

        try:
            long_recurso  = recurso.split('/')[1]
            return HttpResponseRedirect('/json/' + usuario)
        except IndexError:

            num_museos = len(museos_usuario)

            n_paginas = int((num_museos / 5) + 1 )
            ans = "</br> Páginas disponibles:</br>"
            for i in range(1,n_paginas+1):
                 print(str(i))
                 ans += formulario_pagina.format(i)

            resp = ""
            if request.method =='GET':
                for objeto in museos_usuario[:5]:
                    resp += '<li><a href="' + str(objeto.museo.url) + '">' + objeto.museo.nombre + ' en ' + objeto.museo.direccion
                    resp += '</a></br><a href="/museos/' + str(objeto.museo.id) + '">' + "Más información" + '</a> (' + str(objeto.fecha) + ')'
                    resp += "</ul>"
                context = {'titulo': titulo, 'respuesta': resp, 'ans': ans, 'xmlUser': xmlUser}
                #return HttpResponse(titulo + resp + ans + xmlUser)

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
                #return HttpResponse(titulo + resp + ans + xmlUser)
                context = {'titulo': titulo, 'respuesta': resp, 'ans': ans, 'xmlUser': xmlUser}

            return render(request, 'user.html', context)
            #if request.user.is_authenticated() and str(request.user.username) == str(usuario):
            #    print("Aquí tengo las configuraciones en la página de usuario(CSS)")
    except ObjectDoesNotExist:
        error = notOption()
        return HttpResponse(error)



def about(request):
    intro = "Página realizada por Cayetana Gómez Casado."
    funcionamiento = "Aquí tienes las diferentes urls disponibles que te ayudarán a su correcto funcionamiento:"
    context = {'intro': intro, 'funcionamiento': funcionamiento}
    return render(request, 'about.html', context)
