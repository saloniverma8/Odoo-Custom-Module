from odoo import fields, models


class Sale(models.Model):
    _inherit = 'sale.order'
    _description = 'Course_Sales'

    course_id = fields.Many2one('school.course', string='Course Sales')
