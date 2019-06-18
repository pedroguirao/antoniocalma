# -*- coding: utf-8 -*-

from odoo import models, fields, api


class crowfunding_opciones(models.Model):
    _name = "crowfunding_opciones"
    _description = "crowfunding_opciones"

    name = fields.Char('Name')
    tipo = fields.Selection(String='Alcance CRFD',selection=[('inversion','Inversión'),('riesgo','Riesgo'),('pais','País'),('financiación','Financiación'),('premium','Premium')])
    nota = fields.Text('Note')
    icon = fields.Binary('Icon')




