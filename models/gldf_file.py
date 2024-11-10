# models/gldf_file.py
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import os
import tempfile
import gldf_rs_python
import json


class GLDFFile(models.Model):
    _name = 'gldf.file'
    _description = 'GLDF File'
    _inherit = ['mail.thread']

    name = fields.Char(
        string='File Name',
        required=True,
        tracking=True
    )
    upload_date = fields.Datetime(
        string='Upload Date',
        default=fields.Datetime.now,
        tracking=True
    )
    file_data = fields.Binary(
        string='File Data',
        required=True,
        attachment=True
    )
    json_data = fields.Json(
        string='JSON Data',
        readonly=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('processed', 'Processed'),
        ('error', 'Error')
    ], default='draft')

    product_ids = fields.One2many(
        'lighting.product',
        'gldf_file_id',
        string='Products'
    )

    product_count = fields.Integer(
        compute='_compute_product_count',
        string='Product Count'
    )

    @api.depends('product_ids')
    def _compute_product_count(self):
        for record in self:
            record.product_count = len(record.product_ids)

    def action_process_file(self):
        self.ensure_one()
        try:
            with tempfile.NamedTemporaryFile(suffix='.gldf', delete=False) as temp_file:
                file_content = base64.b64decode(self.file_data)
                temp_file.write(file_content)
                temp_file.flush()

                # Convert GLDF to JSON
                json_data = gldf_rs_python.gldf_to_json(temp_file.name)
                self.json_data = json.loads(json_data)

                # Create products from JSON data
                self._create_products_from_json()

                self.state = 'processed'
        except Exception as e:
            self.state = 'error'
            raise ValidationError(f"Failed to process GLDF file: {str(e)}")
        finally:
            if 'temp_file' in locals():
                os.unlink(temp_file.name)

    def _create_products_from_json(self):
        if not self.json_data:
            return

        try:
            product_data = self.json_data.get('ProductDefinitions', {}).get('ProductMetaData', {})
            self.env['lighting.product'].create({
                'name': product_data.get('Name', 'Unknown Product'),
                'description': product_data.get('Description', ''),
                'technical_data': str(product_data.get('technical_data', {})),
                'gldf_file_id': self.id,
                })
        except Exception as e:
            raise ValidationError(f"Failed to create products from JSON: {str(e)}")


# models/lighting_product.py
