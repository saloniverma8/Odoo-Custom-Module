from odoo import fields, models, api
from odoo.exceptions import ValidationError


class EnrollStudentWizard(models.TransientModel):
    _name = 'enroll.student.wizard'
    course_id = fields.Many2one('school.course')
    student_id = fields.Many2one('school.student', string='Students')
    course_date_schedule = fields.One2many(related='course_id.schedule',
                                           string='Course Plan', readonly=True)

    student_schedule = fields.One2many(related='student_id.schedule',
                                       string='Student Plan', readonly=True)
    sale_order = fields.Many2one('sale.order')

    def enroll_student(self):
        for rec in self:
            # this = self
            course_date_start = rec.course_id.start_date
            course_date_end = rec.course_id.end_date

            student_period_start_lst = rec.student_schedule.mapped('start_time')
            student_period_end_lst = rec.student_schedule.mapped('end_time')

            course_period_start = rec.course_id.schedule.mapped('start_time')
            course_period_end = rec.course_id.schedule.mapped('end_time')

            if rec.course_id in list(rec.student_schedule.course_id):
                raise ValidationError('Student already Enrolled!')
            else:
                # print('\nCourse Plan:', course_date_start, '---', course_date_end)
                for i, course_period_start_val in enumerate(
                        course_period_start):
                    # print('\nCourse Periods:\n', course_period_start_val, course_period_end[i])
                    for j, student_period_start_val in enumerate(
                            student_period_start_lst):
                        # print('\nstudent-period-{}'.format(j), student_period_start_val, '---', student_period_end_lst[j])
                        if course_period_start_val == student_period_start_val:
                            raise ValidationError(
                                'Student Cannot be enrolled, Due to Date Collisoin!')
                # "New Student added"
                self.student_id.course_id = [(4, rec.course_id.id)]
                sales = self.env['sale.order'].create({'partner_id': self.student_id.partner_id.id})
                sales.order_line.create({
                    'order_id': sales.id,
                    'name': self.course_id.name,
                    'product_template_id':
                        self.course_id.product_id.product_tmpl_id.id,
                    'product_id': self.course_id.product_id.id,
                    'price_unit': self.course_id.price
                })


                self.sale_order.course_id = rec.course_id
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'sales.action_orders',
                    'view_mode': 'form',
                    'res_model': 'sale.order',
                    'res_id': sales.id,
                    'target': 'current',
                    'context': {
                        'form_view_initial_mode': 'edit',
                                },
                        }