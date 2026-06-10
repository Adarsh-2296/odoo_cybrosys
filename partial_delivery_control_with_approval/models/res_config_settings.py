from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    payment_control_users = fields.Many2many('res.users',string='Control Users')