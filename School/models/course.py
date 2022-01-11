from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, date


class Course(models.Model):
    _name = 'school.course'
    _description = 'Course'

    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    level = fields.Selection(string='Level', selection=[
        ('1', 'A1.1'),
        ('2', 'A1.2'),
        ('3', 'B1.1'),
        ('4', 'B1.2'),
        ('5', 'C1.1'),
        ('6', 'C1.2'),
    ], default='1')
    course_language = fields.Many2one('res.lang', string='Languages')
    name = fields.Char(compute='_create_name', string='Name', store=True)
    price = fields.Monetary(string='Price', digits=(4, 2), required=True,
                            currency_field='currency_id', default=500)
    status = fields.Selection(string='Status', selection=[
        ('open', 'Open'),
        ('inprogress', 'In Progress'),
        ('finished', 'Finished'),
    ], default='open', required=True)
    start_date = fields.Date(string='Start of Course', required=True)
    end_date = fields.Date(string='End of Course', required=True)
    total_hours = fields.Char(string='Credit Hours',
                              compute='_compute_course_info')
    period_count = fields.Integer(compute='_compute_course_info',
                                  string='Total Periods in Course')
    teacher_id = fields.Many2one('school.teacher', string="Course Teacher")

    student_id = fields.Many2many('school.student',
                                  string='Students')
    schedule = fields.One2many('school.period', 'course_id',
                               string='Course Schedule')
    sale_order_ids = fields.One2many('sale.order', 'course_id',
                                     string='Course Sales')
    sales_count = fields.Integer(compute='_compute_sales_course')
    product_id = fields.Many2one('product.product', string='Product')

    @api.constrains('start_date', 'end_date')
    def _check_course_date(self):
        # if self.start_date <= datetime.now():
        #     raise ValidationError('Start date must be after today.')
        if self.end_date <= self.start_date:
            raise ValidationError('End date must be after Start Date')

    @api.depends('schedule')
    def _compute_course_info(self):
        for course in self:
            count = len(course.schedule)
            course.period_count = count
            course.total_hours = 2 * count

    @api.depends('level', 'course_language')
    def _create_name(self):
        for course in self:
            course_level = (
                dict(course._fields['level'].selection).get(course.level))
            if course.level and course.course_language:
                course.name = "%s %s" % \
                              (course.course_language.name, course_level)
            else:
                course.name = ''

    @api.depends('sale_order_ids')
    def _compute_sales_course(self):
        for course in self:
            course.sales_count = len(course.sale_order_ids)

    def sales_order(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'course_Sales',
            'view_mode': 'tree',
            'res_model': 'sale.order',
        }
