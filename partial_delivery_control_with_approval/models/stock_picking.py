from odoo import fields, models, api
from odoo.exceptions import ValidationError

class ProductProduct(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection(selection_add=[('to_approve', 'To Approve'),('approved', 'Approved'),('done',)])
    current_user_allowed = fields.Boolean(string='Current User',compute='_compute_user_allowed')
    current_not_user_allowed = fields.Boolean(string='Not Current User', compute='_compute_user_allowed')

    def button_validate(self):
        if self.picking_type_code != 'incoming' and self.state != 'approved':
            list_product = self.move_ids.filtered(lambda move: not move.product_id.is_allow_partial_delivery and move.product_uom_qty > move.quantity)
            users = self.env['ir.config_parameter'].sudo().get_param('partial_delivery_control_with_approval.payment_control_users')
            if (str(self.env.user.id) in users) or (not list_product):
                return super().button_validate()
            else:
                raise ValidationError('You are not allowed to make partial transfer for this product. Please make a request to the Authorized Person')
        else:
            return super().button_validate()

    def button_request_approve(self):
        list_product = self.move_ids.filtered(
            lambda move: not move.product_id.is_allow_partial_delivery and move.product_uom_qty > move.quantity)
        if list_product:
            self.write({'state': 'to_approve'})
        else:
            raise ValidationError('No need to make a request for approval on this delivery')

    def action_approve_delivery(self):
        users = self.env['ir.config_parameter'].sudo().get_param('partial_delivery_control_with_approval.payment_control_users')
        if str(self.env.user.id) in users:
            self.write({'state': 'approved'})
        else:
            raise ValidationError('You are not allowed to approve delivery.')

    @api.depends('state')
    def _compute_user_allowed(self):
        for rec in self:
            users = self.env['ir.config_parameter'].sudo().get_param('partial_delivery_control_with_approval.payment_control_users')
            if str(self.env.user.id) in users and self.state == 'to_approve':
                rec.current_user_allowed = True
            else:
                rec.current_user_allowed = False
            if str(self.env.user.id) not in users and self.state == 'assigned':
                rec.current_not_user_allowed = True
            else:
                rec.current_not_user_allowed = False