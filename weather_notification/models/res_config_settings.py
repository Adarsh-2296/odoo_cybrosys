from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    current_location = fields.Char(string="Location",config_parameter="weather_notification.current_location")