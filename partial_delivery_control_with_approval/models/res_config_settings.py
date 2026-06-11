from odoo import fields, models,api
from ast import literal_eval

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    payment_control_users = fields.Many2many('res.users',string='Control Users')

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'partial_delivery_control_with_approval.payment_control_users', self.payment_control_users.ids)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        with_user = self.env['ir.config_parameter'].sudo()
        com_contacts = with_user.get_param('partial_delivery_control_with_approval.payment_control_users')
        res.update(payment_control_users=[(6, 0, literal_eval(com_contacts))
                                 ] if com_contacts else False, )
        return res
