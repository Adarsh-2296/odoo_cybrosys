from odoo import models, api

class StockPicking(models.Model):
   _inherit = 'stock.picking'
   @api.model
   def get_tiles_data(self):
       company_id = self.env.company
       result = self.search([('company_id', '=', company_id)]).mapped('name')
       return {'result': result}
