#!/usr/bin/python
# -*- coding: utf-8 -*-
# Programa con la ilusión de poder descargarme automaticamente las facturas de movistar.

import mechanize, urllib2
from urllib import urlopen, urlencode 

# Variables
movistar_user = 'DNI_NUMBER'
movistar_password = 'YOUR_WEB_PASS'
output_file = 'factura_movistar.pdf'

web = "https://www.canalcliente.movistar.es/fwk/cda/controller/CCLI_CW_publico/pub/0,4093,259_1854_200108540_0_0,00.html?s=p&CWEB_URI=https%3A%2F%2Fwww.canalcliente.movistar.es%2Ffwk%2Fcda%2Fcontroller%2FCCLI_CW_privado%2F0%2C2217%2C259_0_2326_0_0%2C00.html"
pagina_facturas = "https://www.canalcliente.movistar.es/fwk/cda/controller/CCLI_CW_privado/0,2217,259_345676826_18435__,00.html"
login_web = "https://sslwb.movistar.es/auth/Login"
fichero_unparsed = "%(url)s?errorODWEK=&sFormato=pdf&sTipoDocumento=%(type)s&sDireccion=%(address)s&sFactura2=%(number)s&sTipoServicio=%(service)s&telefono=%(telid)s&sFecha=%(date)s&sImporte=%(import)s&isPrimera=&filaSeleccionada=0&sAccion=descargar&sOrigen=&sFirma=%(signature)s&sCodigoUsuario=%(username)s&sCnif=%(id)s&iPerfil=%(profile)s&sCodigoCuenta=%(client)s&sCodigoUsuarioEstadisticas=&sFechaTimeStamp=%(now)s&sCodIdentifi=N&sFechaActual=%(today)s&sCifAntiguo=&sFechaMigracion=&sTelefono=&sMenu=&antiCacheo=anticacheo"

# Funciones
def obtener_datos_javascript(html):
	array_factura = []
	dic_fac={}
	for linea in html.split('\n'):
		if 'javascript:abreVentanaDescarga(' in linea:
			array_factura = linea.split('javascript:abreVentanaDescarga(')[1].replace(' ','')[1:-5].split("',")
			for i in range(0,len(array_factura)):
				if array_factura[i][0]=="'": array_factura[i]=array_factura[i][1:]
			break
	dic_fac['certType'] = array_factura[0]
	dic_fac['type'] = array_factura[1]
	dic_fac['address'] = array_factura[2]
	dic_fac['number'] = array_factura[3]
	dic_fac['service'] = array_factura[4]
	dic_fac['date'] = array_factura[5].replace('/','%2F')
	dic_fac['import'] = array_factura[6].replace(',','%2C')
	dic_fac['bool'] = array_factura[7]
	dic_fac['telid'] = array_factura[8]
	dic_fac['now'] = array_factura[9].replace('/','%2F').replace(':','%3A')
	dic_fac['signature'] = array_factura[10]
	dic_fac['url'] = array_factura[11]
	dic_fac['username'] = array_factura[12]
	dic_fac['id'] = array_factura[13]
	dic_fac['profile'] = array_factura[14]
	dic_fac['client'] = array_factura[15]
	dic_fac['today'] = array_factura[17].replace('/','%2F')
	return dic_fac

br = mechanize.Browser()
br.open(web)

data = {
	'OK': '++++OK++++',
	'LOCALE':'en_US',
	'AUTHMETHOD':'UserPassword',
	'pageGenTime':'9999999999999',
	'usr_password':'KjhG3Tv51',
	'pgeac': movistar_password,
	'usr_name':'h%s' %movistar_user,
	'HiddenURI':'https://www.canalcliente.movistar.es/fwk/cda/controller/CCLI_CW_privado/0,2217,259_0_2326_0_0,00.html',
	'cifAntig':''
}

response1 = urllib2.Request(login_web, urlencode(data))

br.open(response1)
br.open(pagina_facturas)
html_facturas = br.response().read()

data = obtener_datos_javascript(html_facturas)

br.open(fichero_unparsed %data)
pdf_factura = open(output_file, 'w')
pdf_factura.write(br.response().read())
pdf_factura.close()
