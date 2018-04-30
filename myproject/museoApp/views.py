from django.shortcuts import render
import urllib.request
import xml.etree.ElementTree as ET
from django.http import HttpResponse

lista={}

def xmlParser(request):
    xml_Url = 'https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?             vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full'
    f = urllib.request.urlopen(xml_Url)
    data = f.read()
    f.close()
    try:
        lista[xml_Url] = data.decode('utf-8')
    except UnicodeDecodeError:
            lista[xml_Url] = data    
   
    #return HttpResponse(lista[xml_Url])

   
    tree = ET.parse(data)
    root = tree.getroot()

#     for child in root:
#        print (child.tag, child.attrib)

#country {'name': 'Liechtenstein'}
#country {'name': 'Singapore'}
#country {'name': 'Panama'}
#Children are nested, and we can access specific child nodes by index:

#>>> root[0][1].text
#'2008'
#19.7.1.3. Finding interesting elements
#Element has some useful methods that help iterate recursively over all the sub-tree below it (its children, their children, and so on). For example, Element.iter():

    for atributo in root.findall('atributo'):
        distrito = atributo.find('distrito').text
        print (distrito)    


#for descripcion in root.iter('descripcion'):
#        print descripcion.attrib

#{'name': 'Austria', 'direction': 'E'}
#{'name': 'Switzerland', 'direction': 'W'}
#{'name': 'Malaysia', 'direction': 'N'}
#{'name': 'Costa Rica', 'direction': 'W'}
#{'name': 'Colombia', 'direction': 'E'}
#Element.findall() finds only elements with a tag which are direct children of the current element. Element.find() finds the first child with a particular tag, and Element.text accesses the element’s text content. Element.get() accesses the element’s attributes:

#    

#Liechtenstein 1
#Singapore 4
#Panama 68
