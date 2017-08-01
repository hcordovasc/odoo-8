# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import time
import datetime
import calendar
from datetime import date, timedelta

url1 = "http://www.asesorempresarial.com/web/efinanzas-tipo-cambio.php"  # change to whatever your url is
page1 = urllib2.urlopen(url1).read()
# print (page)
soup1 = BeautifulSoup(page1, "lxml")
mes_cambio = soup1.find_all('select', attrs={'id': 'mes'})[0].find_all('option', selected=True)
anio_cambio = soup1.find_all('select', attrs={'id': 'ano'})[0].find_all('option', selected=True)
for mc in mes_cambio:
    mcambio = mc['value']
for ac in anio_cambio:
    acambio = ac['value']


url = "http://www.asesorempresarial.com/web/efinanzas-tipo-cambio.php?ano="+acambio+"&mes="+mcambio+"&button2=Actualizar&type=#data"  # change to whatever your url is

anio_i = url.find('ano=')
anio_f = url.find('&')
mes_i = url.find('mes=')
mes_f = url.find('&button2')
anio_cambio = url[anio_i+4:anio_f]
mes_cambio = url[mes_i+4:mes_f]

page = urllib2.urlopen(url).read()
# print (page)
soup = BeautifulSoup(page, "lxml")
# mes_cambio = soup.find_all('select', attrs={'id':'mes'})[0].find_all('option', selected= True)
# anio_cambio = soup.find_all('select', attrs={'id':'ano'})[0].find_all('option', selected= True)
# print (mes_cambio)
# print (anio_cambio)

# tablita = soup.prettify()[28970::]
print ('-----------------')
# soup = BeautifulSoup(tablita, "lxml")

dias = []
compra = []
venta = []
today = datetime.datetime.now()

for fila in soup.find_all(name='table')[15].find_all(name='tr')[2:-1]:
    # print fila
    cambio_dia = fila.findAll('td')[0].div.text.strip()
    cambio_compra = fila.findAll('td')[5].div.text.strip()
    cambio_venta = fila.findAll('td')[6].div.text.strip()
    dias.append(cambio_dia)
    compra.append(cambio_compra)
    venta.append(cambio_venta)
    # print (cambio_dia, cambio_compra, cambio_venta)
# # print (dias)
# # print (compra)
# # print (venta[-1])
# # print (dias, compra, venta)
ini = -1
for dia in dias:
    ini += 1
    f = str('%s-%s-%s') % (anio_cambio, str(mes_cambio).zfill(2), dia.zfill(2))
    # print ('f', str(f))
    slist = f.split("-")
    sdate = datetime.date(int(slist[0]), int(slist[1]), int(slist[2]))
    valor_soles_compra = 1 / float(compra[ini])
    valor_soles_venta = 1 / float(venta[ini])
    print (f, valor_soles_compra, valor_soles_venta)
