from odoo import http
from odoo.http import request


class AppointmentController(http.Controller):

    @http.route('/om_hospital/appointments', type='json', auth='user')
    def appointment_banner(self):
        return {
            'html': """
                <div style="text-align:center; padding:10px; background:#f4f6f7; border-bottom:1px solid #ddd;">

                    <h2 style="color:#e74c3c;">
                        Welcome To Om-Hospital...!
                    </h2>

                    <p>
                        <a href="https://www.youtube.com/channel/UCVKLUZP7HAhdQgs-9iTJklQ/videos"
                           target="_blank"
                           style="color:#3498db; font-weight:bold;">
                            Get Notified Regarding All The Odoo Updates!
                        </a>
                    </p>

                </div>
            """
        }


class Hospital(http.Controller):

    @http.route('/patient_webform', type="http", auth="public", website=True)
    def patient_webform(self, **kw):
        return http.request.render('om_hospital.create_patient', {})

    @http.route('/create/webpatient', type='http', auth="public", website=True)
    def create_webpatient(self, **kw):
        request.env['hospital.patient'].sudo().create(kw)
        return request.render("om_hospital.patient_thanks", {})

