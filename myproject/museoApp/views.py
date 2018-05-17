from django.shortcuts import render
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from django.http import HttpResponse
from .models import *


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
                        if accesibilidad == 0:
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

        #museo.save()
    #return HttpResponseRedirect('/')
