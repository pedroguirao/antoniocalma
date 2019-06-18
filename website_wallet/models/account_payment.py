# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_paid(self):
        res = super(AccountInvoice, self).action_invoice_paid()

        # refund to wallet when paid invoice
        for inv in self:
            if inv.type in ['in_refund', 'out_refund']:
                if self.origin:
                    origin_inovice_id = self.search([('number', '=', self.origin)])
                    if origin_inovice_id:
                        sale_order_id = self.env['sale.order'].search([('name', '=', origin_inovice_id.origin)])
                        if sale_order_id.wallet_txn_id:
                            acquirer = self.env['payment.acquirer'].sudo().search([
                                ('is_wallet_acquirer', '=', True)], limit=1)
                            if not acquirer:
                                raise UserError(_('No acquirer configured. Please create wallet acquirer.'))
                            vals = {
                                'acquirer_id': acquirer.id,
                                'type': 'form',
                                'amount': sale_order_id.wallet_txn_id.amount,
                                'currency_id': sale_order_id.company_id.currency_id.id,
                                'partner_id': sale_order_id.partner_id.id,
                                'partner_country_id': sale_order_id.partner_id.country_id.id,
                                'is_wallet_transaction': True,
                                'wallet_type': 'credit',
                                'sale_order_id': sale_order_id.id,
                                'reference': self.env['payment.transaction'].get_next_wallet_reference(),
                            }
                            tx = self.env['payment.transaction'].sudo().create(vals)
                            tx.state = 'done'
        return res
