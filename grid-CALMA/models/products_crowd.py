# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductsCrowd(models.Model):
    _inherit = "product.template"

    zona = fields.Char('Zona')
    crfd = fields.Char('Alcance CRFD')
    tipo_inversion = fields.Many2one(String='Tipo Inversión',comodel_name='crowfunding_opciones',domain=('tipo','=','inversion'))
    riesgo_inversion = fields.Many2one(String='Riesgo Inversión',comodel_name='crowfunding_opciones',domain=('tipo','=','riesgo'))
    pais = fields.Many2one(String='País',comodel_name='crowfunding_opciones',domain=('tipo','=','pais'))
    financiacion_bancaria = fields.Many2one(String='Financiación Bancaria',comodel_name='crowfunding_opciones',domain=('tipo','=','financiacion'))
    premium = fields.Many2one(String='Premium',comodel_name='crowfunding_opciones',domain=('tipo','=','premium'))
    objetivo_crowfunding = fields.Float('Objetivo Crowfunding')
    invertido = fields.Float('Invertido')
    porcentaje_crowfunding = fields.Float('Porcentaje Crowfunding')
    inversores = fields.Integer('Inversores')
    plazo_inversion = fields.Char('Plazo Inversión')
    rentabilidad_anual = fields.Char('Rentabilidad Anual')
    tir_historico = fields.Char('TIR Histórico')
    rentabilidad_total = fields.Char('Rentabilidad Total')
    mapa = fields.Binary('Mapa')




