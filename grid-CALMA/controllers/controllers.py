# -*- coding: utf-8 -*-

from odoo import http
from openerp.addons.website_sale.controllers import main


# class Extra-addons/miModulo(http.Controller):
#     @http.route('/extra-addons/mi_modulo/extra-addons/mi_modulo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/extra-addons/mi_modulo/extra-addons/mi_modulo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('extra-addons/mi_modulo.listing', {
#             'root': '/extra-addons/mi_modulo/extra-addons/mi_modulo',
#             'objects': http.request.env['extra-addons/mi_modulo.extra-addons/mi_modulo'].search([]),
#         })

#     @http.route('/extra-addons/mi_modulo/extra-addons/mi_modulo/objects/<model("extra-addons/mi_modulo.extra-addons/mi_modulo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('extra-addons/mi_modulo.object', {
#             'object': obj
#         })