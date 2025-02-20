# coding: utf-8
from odoo import fields, models

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Property"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string ="Available From",copy=False, default=lambda self:fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(selection=[('east', "East"), ('north', "North"), ('south', "South"), ('west', "West")])
    state = fields.Selection(required=True, default='new', copy=False,
        selection=[('new', "New"), ('received', "Offer Received"), ('accepted', "Offer Accepted"), ('sold', "Sold"), ('canceled', "Canceled")])
    active = fields.Boolean(default=True)