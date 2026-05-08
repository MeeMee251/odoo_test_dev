import base64

from odoo import models,fields,api, _
from odoo.exceptions import ValidationError

class ResPartners(models.Model):
    _inherit = "res.partner"

    @api.model
    def create(self, vals_list):
        res= super(ResPartners, self).create(vals_list)
        print("yes working")
        #do the custom coding here
        return res

    company_type = fields.Selection(selection_add=[('om','Odoo Mates'), ('odoodev','OdooDev')])


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        print("Odoo Mates")
        res = super(SaleOrderInherit, self).action_confirm()
        return res


    patient_name = fields.Char(string="Patient Name")

    def get_sale_pdf(self):
        report = self.env.ref('sale.action_report_saleorder')
        pdf, _ = report.render_qweb_pdf(self.ids)
        return base64.b64encode(pdf)

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Patient Record"
    _rec_name = 'patient_name'

    def action_patients(self):
        print("ggg")
        return {
            'name': _('Patients Server Action'),
            'domain': [],
            'view_type': 'form',
            'res_model': 'hospital.patient',
            'view_id' : False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }

    @api.multi
    def print_report(self):
        return self.env.ref('om_hospital.report_patient_card').report_action(self)

    @api.multi
    def print_report_excel(self):
        return self.env.ref('om_hospital.report_patient_card_xlsx').report_action(self)

    @api.model
    def test_cron_job(self):
        print("test_cron_job")
        #code accordingly to execute the cron

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' %(rec.name_seq, rec.patient_name)))
        return res

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result

    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age:
                if rec.patient_age < 18:
                    rec.age_group = 'minor'
                else:
                    rec.age_group = 'major'

    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValidationError(_('Patient Age must be greater than 5'))

    def open_patient_appointments(self):
        return{
            'name':_('Appointments'),
            'domain':[('patient_id', '=', self.id)],
            'view_type':'form',
            'res_model':'hospital.appointment',
            'view_mode': 'tree,form',
            'type':'ir.actions.act_window'
        }

    def get_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count(
                [('patient_id', '=', rec.id)]
            )

    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        # print("entering")
        for rec in self:
            if rec.doctor_id:
                rec.doctor_gender = rec.doctor_id.gender

    def action_send_card(self):
        print("sending email")
        template_id = self.env.ref('om_hospital.patient_card_email_template').id
        print("template id",template_id)
        template = self.env['mail.template'].browse(template_id)
        print("template", template)
        template.send_mail(self.id, force_send=True)

    @api.depends('patient_name')
    def _compute_upper_name(self):
        for rec in self:
            rec.patient_name_upper = rec.patient_name.upper() if rec.patient_name else False

    def _inverse_upper_name(self):
        for rec in self:
            rec.patient_name = rec.patient_name_upper.lower() if rec.patient_name_upper else False

    patient_name = fields.Char(string="Name", required=True, track_visibility='always')
    patient_age = fields.Integer('Age', track_visibility='always', group_operator=False)
    patient_age2 = fields.Float(string="Age 2")
    notes = fields.Text(string="Registration Notes")
    image = fields.Binary(string="Image", attachment=True)
    name = fields.Char(string="Test")
    cont_num = fields.Integer(string="Contact Number")
    name_seq = fields.Char(string='Order Reference', required = True, copy=False, readonly=True,
                           index=True, default=lambda self:_('New'))

    appointment_count = fields.Integer(string="Appointment", compute='get_appointment_count')
    active = fields.Boolean(default=True, string="Active")

    doctor_id = fields.Many2one('hospital.doctor',string="Doctor")
    doctor_gender = fields.Selection(related='doctor_id.gender',string="Doctor Gender")

    user_id = fields.Many2one('res.users', string="PRO")
    patient_email = fields.Char(string="Email")

    patient_name_upper = fields.Char(compute="_compute_upper_name", inverse='_inverse_upper_name')

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ],default='male',string="Gender" )

    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor'),
    ], string="Age Group", compute='set_age_group', store=True)

