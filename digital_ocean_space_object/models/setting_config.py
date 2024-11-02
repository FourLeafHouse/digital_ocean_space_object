from odoo import fields, models, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'Res Config Settings'

    access_key = fields.Char(config_parameter='access_key')
    secret_key = fields.Char(config_parameter='secret_key')