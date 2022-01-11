# from odoo import api, models
#
#
# class StudentReport(models.AbstractModel):
#
#     _name = 'report.school.student.report'
#     _description = 'Student Report'
#
#     @api.model
#     def _get_report_values(self, docids, data=None):
#         print('************************* we are here %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
#         print('docids', docids)
#         docs = self.env['School.student'].browse(docids[0])
#
#         return {
#             'doc_model': 'School.student',
#             'data': data,
#             'docs': docs,
#             }
