from odoo import http
from odoo.http import request

class ClearCart(http.Controller):
    @http.route(['/shop/cart/removeall'], type='http',auth="public", website=True)
    def clear_cart_products(self, **kw):
        partner_id = self.env.user.partner_id
        orders = request.website._order
        print(orders)
        order = self.env['sale.order'].sudo().search([('partner_id.id','=',partner_id),('website_id','!=',False,)])
        order.sudo().unlink()
        return request.render("website_sale.cart")