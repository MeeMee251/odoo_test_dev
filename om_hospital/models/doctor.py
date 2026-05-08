from odoo import models, fields, api, _

class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Doctor"
    _rec_name = 'doctor_name'

    doctor_name = fields.Char(string="Name", required=True, track_visibility='always')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender", default='male', track_visibility='always')
    user_id = fields.Many2one('res.users', string="Related User")

    appointment_ids = fields.Many2many('hospital.appointment', 'hospital_patient_rel', 'doctor_id_rec', 'appointment_id',
                                  string="Appointments")

    @api.model
    def create(self, vals):
        record = super(HospitalDoctor, self).create(vals)
        return record