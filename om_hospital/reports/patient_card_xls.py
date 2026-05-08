from odoo import models

class PatientCardXLS(models.AbstractModel):
    _name = "report.om_hospital.report_patient_xlsx"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, lines):

        sheet = workbook.add_worksheet('Patient Card')

        sheet.right_to_left()

        header_format = workbook.add_format({
            'font_size': 14,
            'bold': True,
            'align': 'center'
        })

        normal_format = workbook.add_format({
            'font_size': 10,
            'align': 'left'
        })

        sheet.set_column(0, 0, 15)
        sheet.set_column(1, 1, 5)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 20)

        sheet.write(0, 0, "Name", header_format)
        sheet.write(0, 1, "Age", header_format)
        sheet.write(0, 2, "Email", header_format)
        sheet.write(0, 3, "Notes", header_format)

        row = 1

        for patient in lines:
            sheet.write(row, 0, patient.patient_name, normal_format)
            sheet.write(row, 1, patient.patient_age, normal_format)
            sheet.write(row, 2, patient.patient_email, normal_format)
            sheet.write(row, 3, patient.notes, normal_format)
            row += 1