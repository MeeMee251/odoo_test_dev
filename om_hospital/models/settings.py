from odoo import models,fields,api, _
from ast import literal_eval

class HospitalSettings(models.TransientModel):
    _inherit = "res.config.settings"

    note = fields.Char(string="Default Note")
    module_crm = fields.Boolean(string="CRM")
    product_id = fields.Many2many('product.product', string="Medicines")

    def set_values(self):
        res = super(HospitalSettings, self).set_values( )
        self.env['ir.config_parameter'].set_param('om_hospital.note', self.note)
        print("test", self.product_id.ids)
        self.env['ir.config_parameter'].set_param('om_hospital.product_id', self.product_id.ids)
        return res

    @api.model
    def get_values(self):
        res = super(HospitalSettings, self).get_values( )
        ICPSudo = self.env['ir.config_parameter'].sudo()
        notes = ICPSudo.get_param('om_hospital.note')
        product_id = self.env['ir.config_parameter'].sudo().get_param('om_hospital.product_id')
        print("product_id", product_id)
        res.update(
            note = notes,
            product_id = [[6, 0, literal_eval(product_id)]]
        )
        return res