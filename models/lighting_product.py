from odoo import models, fields

class LightingProduct(models.Model):
    _name = 'lighting.product'
    _description = 'Lighting Product'
    _inherit = ['mail.thread']

    name = fields.Char(
        string='Product Name',
        required=True,
        tracking=True
    )
    description = fields.Text(
        string='Description',
        tracking=True
    )
    technical_data = fields.Text(
        string='Technical Data',
        tracking=True
    )
    gldf_file_id = fields.Many2one(
        'gldf.file',
        string='GLDF File',
        ondelete='cascade'
    )
    active = fields.Boolean(
        default=True,
        tracking=True,
        help="If unchecked, it will allow you to hide this record without removing it."
    )