import pdb

import pytz

from odoo import models,fields,api, _

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Patient Appointment"
    _order = "appointment_date desc"

    def test_recordset(self):
        for rec in self:
            print("Odoo ORM: Record Set Operation")
            partners = self.env['res.partner'].search([])
            print("Mated partners...",partners.mapped('phone'))
            print("Sorted partners...", partners.sorted(lambda O: O.write_date, reverse=True))
            print("Filtered partners...", partners.filtered(lambda O: not O.customer))


    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return{'domain' : {'order_id' : [('partner_id','=',rec.partner_id.id)]}}

    # @api.model
    # def default_get(self, fields):
    #     res= super(HospitalAppointment,self).default_get(fields)
    #     print("test...")
    #     res['patient_id'] = 4
    #     res['notes'] = 'Like and Subscribe our channel'
    #     return res

    @api.model
    def default_get(self, fields_list):
        # pdb.set_trace()
        res = super(HospitalAppointment, self).default_get(fields_list)

        appointment_lines = []

        product_rec = self.env['product.product'].search([])

        for product in product_rec:
            line = (0, 0, {
                'product_id': product.id,
                'product_uom_qty': 1,
            })

            appointment_lines.append(line)

        res.update({
            'appointment_lines': appointment_lines,
            'patient_id': 1,
            'notes': 'Like and Subscribe our channel to get notified'
        })
        # print(res['appointment_lines'])
        return res


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result

    @api.model
    def auto_complete_appointments(self):
        appointments = self.search([
            ('appointment_date', '<', fields.Datetime.now()),
            ('state', '=', 'confirm')
        ])
        appointments.write({'state': 'done'})

    @api.multi
    def write(self, vals):
        res = super(HospitalAppointment, self).write(vals)
        print("Test write function")
        # do as per the need
        return res

    # @api.multi
    # def write(self, vals):
    #     for rec in self:
    #         print("Before update:", rec.name, rec.state)
    #     res = super(HospitalAppointment, self).write(vals)
    #     for rec in self:
    #         print("After update:", rec.name, rec.state)
    #     return res

    def _get_default_note(self):
        return "Subscribe our hospital appointment channel and like it"

    def delete_lines(self):
        for rec in self:
            # print("Time in UTC", rec.appointment_datetime)
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            # print("user_tz", user_tz)
            date_today = pytz.utc.localize(rec.appointment_datetime).astimezone(user_tz)
            # print("Time in Local Timezone .. ", date_today)
            rec.appointment_lines = [(5,0,0)]

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Appointment Confirmed...Thank You!',
                    'type': 'rainbow_man',
                }
            }

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_notify(self):
        for rec in self:
            rec.doctor_id.user_id.notify_warning(message='Appointment is confirmed.')

    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     for rec in self:
    #         lines = [(5, 0, 0)]
    #         # lines = [ ]
    #         for line in self.product_id.product_variant_ids:
    #             val = {
    #                 'product_id': line.id,
    #                 'product_uom_qty': 5
    #             }
    #             lines.append((0, 0, val))
    #         rec.appointment_lines = lines

    name = fields.Char(string="Appointment ID", required=True, copy=False, readonly=True,
                       index=True, default=lambda self:_('New'))
    patient_id = fields.Many2one('hospital.patient',string="Patient", required=True)
    patient_age = fields.Integer('Age', related='patient_id.patient_age')
    notes = fields.Text(string="Registration Notes", default = _get_default_note)
    appointment_date = fields.Date(string="Date")
    appointment_date_end = fields.Date(string="End Date")
    appointment_datetime = fields.Datetime(string="Date Time")
    partner_id = fields.Many2one('res.partner',string="Customer")
    order_id = fields.Many2one('sale.order', string="Sale Order")
    product_id = fields.Many2one('product.template', string="Product Template")
    doctor_note = fields.Text(string="Notes")
    pharmacy_note = fields.Text(string="Notes")
    appointment_lines = fields.One2many('hospital.appointment.lines','appointment_id',string="Appointment Lines")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
        ], string='Status',required=True, readonly=True, default='draft')

    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    doctor_ids = fields.Many2many('hospital.doctor', 'hospital_patient_rel', 'appointment_id', 'doctor_id_rec', string="Doctors")
    amount = fields.Float(string="Total Amount")


class HospitalAppointmentLines(models.Model):
    _name = "hospital.appointment.lines"
    _description = "Appointment Lines"

    product_id = fields.Many2one('product.product', string="Medicine")
    product_uom_qty = fields.Integer('Quantity')
    sequence = fields.Integer('Sequence')
    appointment_id = fields.Many2one('hospital.appointment',string="Appointment ID")
