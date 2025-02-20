from odoo import models, fields

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    manager_level = fields.Selection([
        ('1', 'Level 1'),
        ('2', 'Level 2'),
        ('admin', 'Administrator')
    ], string='Management Level')

    # Gérer la limite de confirmation (partie 4 de l'énoncer)      pour définir la limite de confirmation pour cet employé.
    confirmation_limit = fields.Float('Confirmation Limit')