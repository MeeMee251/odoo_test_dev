from odoo import models,fields,api, _

class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    patient_id = fields.Many2one('hospital.patient', string="Patient")
    appointment_date = fields.Date(string="Appointment Date")

    def print_report(self):
        print("kkk--->",self.read()[0])
        data = {
                'model': 'create.appointment',
                'form': self.read()[0]
            }
        # if data['form']['patient_id']:
        #     selected_patient = data['form']['patient_id'][0]
        #     appointments = self.env['hospital.appointment'].search([('patient_id','=',selected_patient)])
        # else:
        #     appointments = self.env['hospital.appointment'].search([])
        # appointment_list = []
        # for app in appointments:
        #     vals = {
        #         'name': app.name,
        #         'notes': app.notes,
        #         'appointment_date': app.appointment_date
        #     }
        #     appointment_list.append(vals)
        #     print("appointments", appointments)
        # data['appointments'] = appointment_list
        # print("Data",data)
        return self.env.ref('om_hospital.report_appointment').with_context(landscape=False).report_action(self, data=data)

    def delete_patient(self):
        for rec in self:
            rec.patient_id.unlink()

    def create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'appointment_date': self.appointment_date,
            'notes' : 'Created From The Wizard/Code'
        }
        self.patient_id.message_post(body="Appointment Created", subject="Appointment")
        new_appointment = self.env['hospital.appointment'].create(vals)
        context = dict(self.env.context)
        context['form_view_initial_mode'] = 'edit'
        return{'type': 'ir.actions.act_window',
               'view_type': 'form',
               'view_mode': 'form',
               'res_model': 'hospital.appointment',
               'res_id': new_appointment.id,
               'context': context}


    def get_data(self):
        print("Get Data Function")
        appointments = self.env['hospital.appointment'].search([('patient_id','=',1)])
        print("appointments:", appointments)
        for rec in appointments:
            print("Appointment Name:", rec.name)
        # return {
        #     "type": "ir.actions.do_nothing"
        # }
