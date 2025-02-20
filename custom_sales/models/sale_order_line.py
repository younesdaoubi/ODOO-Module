from . import sale_order_line

from odoo import models, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    training_date = fields.Date(string='Training Date')
    employee_id = fields.Many2one('hr.employee', string='Assigned Employee')