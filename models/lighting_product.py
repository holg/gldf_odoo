from odoo import models, fields

class LightingProduct(models.Model):
    _name = 'lighting.product'
    _description = 'Lighting Product'

    name = fields.Char(string='Product Name', required=True)
    description = fields.Text(string='Description')
    technical_data = fields.Text(string='Technical Data')
    gldf_file_id = fields.Many2one('gldf.file', string='GLDF File')