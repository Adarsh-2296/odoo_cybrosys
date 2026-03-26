from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    order_line_limit = fields.Boolean(config_parameter="purchase.order_line_limit",string="Set Order Line Limit")