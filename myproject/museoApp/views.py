from django.shortcuts import render
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from django.http import HttpResponse


def xmlParser(request):
    print("Estoy en parser")
    xml_Url = "https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full"
    page = urlopen(xml_Url)
    tree = ET.parse(page)
    root = tree.getroot()
   
    for i in root.iter('contenido'):
        for j in i.iter('atributos'):
            for k in j.findall('atributo'):
                try:
                    name = k.find('[@nombre="NOMBRE"]').text
                    print ("name:" + name)
                    descripcion = k.find('[@nombre="DESCRIPCION-ENTIDAD"]').text
                    print ("descripcion: " + descripcion)        
                    distrito = k.find('[@nombre="DISTRITO"]').text
                    print ("distrito: " + distrito)
                except AttributeError:
                    pass
        

