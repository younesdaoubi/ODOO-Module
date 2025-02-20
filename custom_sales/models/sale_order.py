from odoo import models, fields, api, exceptions
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    #champ calculé pour déterminer le niveau d'approbation requis pour la commande.

    approval_level_required = fields.Selection([
        ('0', 'None'),
        ('1', 'Level 1'),
        ('2', 'Level 2'),
        ('admin', 'Administrator')
    ], string='Approval Level Required', compute='_compute_approval_level', store=True)

    # Méthode de calcul pour définir le niveau d'approbation en fonction du montant total de la commande. ( point 3 de l'enoncer)
    @api.depends('amount_total')
    def _compute_approval_level(self):
        for order in self:
        # Définir le niveau d'approbation en fonction des différents seuils du montant total.
            if order.amount_total < 500:
                order.approval_level_required = '0'
            elif order.amount_total < 1000:
                order.approval_level_required = '1'
            elif order.amount_total < 5000:
                order.approval_level_required = '2'
            else:
                order.approval_level_required = 'admin'
        # Action pour demander l'approbation de la commande de vente.
    def action_request_approval(self):
        for order in self:
            if order.approval_level_required == '0':
                order.action_confirm()
            else:
                group_xml_id = 'custom_sales.group_manager_level_%s' % order.approval_level_required
                group = self.env.ref(group_xml_id)
                users = group.users
                for user in users:
                    order.activity_schedule(
                        'mail.mail_activity_data_todo',
                        user_id=user.id,
                        summary='Approval Required',
                        note=f'Please approve this Quotation: {order.name}'
                    )
                order.message_post(body="Approval requested from managers.")

    def action_confirm(self):
        # Appel de la méthode super pour conserver le comportement original
        res = super(SaleOrder, self).action_confirm()

        # Création des événements de calendrier pour les lignes de formation
        for line in self.order_line:
                _logger.info(f"Creating calendar event for training: {line.product_id.name}, Date: {line.training_date}")
                self.env['calendar.event'].create({
                    'name': f'Formation: {line.product_id.name}',
                    'start': line.training_date,
                    'stop': line.training_date,
                    'allday': True,
                    'partner_ids': [(4, line.employee_id.user_id.partner_id.id)]
                })

        return res
    

  
    #La Quotation ne peut être confirmée car le montant total dépasse la limite fixée pour cet employé.

    # Surcharge de la méthode create pour ajouter une vérification de la limite de confirmation.
    @api.model
    def create(self, vals):
        record = super(SaleOrder, self).create(vals)
        record._check_confirmation_limit()
        return record
    # Surcharge de la méthode write pour ajouter une vérification de la limite de confirmation.
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        self._check_confirmation_limit()
        return res
    # Vérifier si le montant total de la commande dépasse la limite de confirmation de l'employé.
    def _check_confirmation_limit(self):
        for record in self:
            if record.user_id.employee_ids:
                employee = record.user_id.employee_ids[0]  # Prendre le premier employé lié à l'utilisateur
                if employee.confirmation_limit and record.amount_total > employee.confirmation_limit:
                    raise exceptions.ValidationError(
                        "La Quotation ne peut être confirmée car le montant total dépasse la limite fixée pour cet employé."
                    )
