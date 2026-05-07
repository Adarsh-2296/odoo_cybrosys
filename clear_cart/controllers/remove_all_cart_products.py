from odoo import http
from odoo.http import request
from werkzeug.utils import redirect


class ClearCart(http.Controller):
    @http.route(['/shop/cart/removeall'], type='http',auth="public", website=True)
    def clear_cart_products(self, **kw):
        """Function to clear all products in the cart on button click"""
        orders = request.cart
        print(orders)
        orders.sudo().unlink()
        return redirect("/shop/cart")