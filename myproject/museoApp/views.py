from django.shortcuts import render
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from django.http import HttpResponse


def xmlParser(request):
    print("Estoy en parser")
    xml_Url = "https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full"
    page = urlopen(xml_Url)
    print("page: " + str(page))
    tree = ET.parse(page)
    print("tree: " + str(tree))
    root = tree.getroot()
    
    for i in root.findall('contenidos'):
        for j in i.findall('atributos'):
            for atributo in j.findall('atributo'):
                name = atributo.find(nombre="NOMBRE").text
                print ("name: " + name)
                descripcion = atributo.find(nombre="DESCRIPCION").text
                print ("descripcion: " + descripcion)        
                distrito = atributo.find(nombre="DISTRITO").text
                print ("distrito: " + distrito)
                resp = str(name) + str(descripcion) + str(distrito)
                return HttpResponse(resp, "200 OK")

