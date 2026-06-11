from odoo import fields, models, api
from odoo.exceptions import ValidationError

class ProductProduct(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for default=lambda self: self.env.company)the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")
    current_user_allowed = fields.Boolean(string='Current User',compute='_compute_user_allowed')

    def button_validate(self):
        print(self.current_user_allowed)
        # if self.picking_type_code != 'incoming' and self.state != 'approved':
        #     print(self.move_ids)
        #     list_product = self.move_ids.filtered(lambda move: not move.product_id.is_allow_partial_delivery and move.product_uom_qty > move.quantity)
        #     print(list_product)
        #     users = self.env['ir.config_parameter'].sudo().get_param('partial_delivery_control_with_approval.payment_control_users')
        #     if (str(self.env.user.id) in users) or (not list_product):
        #         return super().button_validate()
        #     else:
        #         raise ValidationError('You are not allowed to make partial transfer for this product.')
        # else:
        #     return super().button_validate()

    def button_request_approve(self):
        self.write({'state': 'to_approve'})

    def action_approve_delivery(self):
        users = self.env['ir.config_parameter'].sudo().get_param('partial_delivery_control_with_approval.payment_control_users')
        if (str(self.env.user.id) in users) or (not users):
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