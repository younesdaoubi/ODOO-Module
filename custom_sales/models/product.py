# custom_sales/models/product.py
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_training = fields.Boolean(string='Is Training Product', default=False)
