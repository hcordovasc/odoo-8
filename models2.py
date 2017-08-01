# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import except_orm
import urllib2
from bs4 import BeautifulSoup
import time
import datetime
import calendar
from datetime import date, timedelta

from openerp import tools


# clase para heredar el modulo de las tasas moneda
class scraping_currency(models.Model):
    _inherit = 'res.currency.rate'

    name = fields.Date('Date')

    rate_compra = fields.Float(string="Tasa Venta", digits=(12, 6), )
    tc_compra_rate = fields.Float(string="Precio Venta Soles", digits=(12, 6), )
    tc_venta_rate = fields.Float(string="Precio Compra Soles", digits=(12, 6), )

    _defaults = {
        'name': None
    }


# clase para heredar el modulo de monedas general
class scraping_currency(models.Model):

    _inherit = 'res.currency'

    ratio_silent_venta = fields.Float(string='Ratio Actual Venta', digits=(12,6), compute='_get_current_rate2', store= True)


    # funcionar para traer los valores de compra y venta de sunat
    @api.multi
    def button_verificar(self):
        print ('Actualizandoooooooo!')
        currency_br = self.env['res.currency'].browse(self.id)[0]
        if currency_br.name.upper() != 'USD':
            raise except_orm(_('Error!'),
                             _("Por el momento solo funciona para Dolares (USD).\nDisculpa las Molestias :( "))
        else:
            url = "http://www.sunat.gob.pe/cl-at-ittipcam/tcS01Alias"  # Conectarse a la pagina de sunat

            page = urllib2.urlopen(url).read()
            # print (page)
            soup = BeautifulSoup(page, "lxml")
            # print (soup)
            print ('-----------------')
            table = soup.find('table', attrs={'class': 'class="form-table"'})
            # print (table)
            # print (column_headers)
            dias = []
            lst = []
            compra = []
            venta = []
            today = datetime.datetime.now()
            # buscar los valores en toda la pagina
            for tr in table.find_all(name='tr')[-6::]:
                d = tr.findAll("strong")
                tds = tr.findAll("td", attrs={'class': 'tne10'})
                # print (tds)
                for strong in d:
                    dias.append(strong.text)
                for c in tds:
                    lst.append(c.text.strip())
                # print (lst)
            for a in range(len(lst)):
                if a % 2 == 0:
                    compra.append(lst[a])
                elif a % 2 != 0:
                    venta.append(lst[a])

            anio = today.year
            mes = today.month
            ini = -1
            # print (compra)
            # print (venta)

            for dia in dias:
                ini += 1
                f = str('%s-%s-%s') % (anio, mes, dia.zfill(2))
                # print ('date',str(self.name))
                print ('f', str(f))
                # if self.name == f:
                self._cr.execute(
                    """ DELETE FROM res_currency_rate WHERE name = %s""",[f])  # eliminar valores de la tabla para poder actualizar los valores
                slist = f.split("-")
                sdate = datetime.date(int(slist[0]), int(slist[1]), int(slist[2]))
                valor_soles_compra = 1 / float(compra[ini])
                valor_soles_venta = 1 / float(venta[ini])
                # print (sdate, '/', valor_soles_compra, '/', valor_soles_venta)
                # guardar los valores en un diccionario para guardarlos
                valores = {
                    'currency_id': self.id,
                    'name': sdate,
                    'rate': valor_soles_compra,
                    'rate_compra': valor_soles_venta,
                    'tc_compra_rate': float(venta[ini]),
                    'tc_venta_rate': float(compra[ini]),
                }
                # print (valores)

                self.env['res.currency.rate'].create(valores)  # guardar los valores en la tabla directamente

        return self.write({'tc_compra': float(compra[-1]), 'tc_venta': float(venta[-1])})  # refrescar la pagina

    @api.one
    @api.depends('rate_ids')
    def _get_current_rate2(self, context=None):
        # print ('ghghgggfgfgfgf')
        date = self._context.get('date') or time.strftime('%Y-%m-%d')
        self._cr.execute('SELECT rate_compra FROM res_currency_rate '
                   'WHERE currency_id = %s '
                     'AND name <= %s '
                   'ORDER BY name desc LIMIT 1',
                   (self.id, date))
        if self._cr.rowcount:
            self.ratio_silent_venta = self._cr.fetchone()[0]
        else:
            self.ratio_silent_venta = 0

