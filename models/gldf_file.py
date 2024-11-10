from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import gldf_rs_python

class GLDFFile(models.Model):
    _name = 'gldf.file'
    _description = 'GLDF File'

    name = fields.Char(string='File Name', required=True)
    upload_date = fields.Datetime(string='Upload Date', default=fields.Datetime.now)
    file_data = fields.Binary(string='File Data', required=True)
    json_data = fields.Text(string='JSON Data', readonly=True)
    product_ids = fields.One2many('lighting.product', 'gldf_file_id', string='Products')

    @api.model
    def create(self, vals):
        try:
            # Decode the uploaded file
            file_content = base64.b64decode(vals['file_data'])
            file_path = '/tmp/uploaded_file.gldf'

            # Save the file temporarily
            with open(file_path, 'wb') as f:
                f.write(file_content)

            # Use gldf_rs_python to convert GLDF to JSON
            json_data = gldf_rs_python.gldf_to_json(file_path)
            vals['json_data'] = json_data
        except Exception as e:
            raise ValidationError(f"Failed to process GLDF file: {str(e)}")

        # Create the GLDFFile record
        return super(GLDFFile, self).create(vals)