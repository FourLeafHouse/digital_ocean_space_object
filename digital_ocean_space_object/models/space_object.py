from odoo import fields, models, api

class SpaceObject(models.Model):
    _name = 'do.space.object'
    _description = 'DO Space Object'

    name = fields.Char('Space Name')
    region = fields.Char('Region')