from odoo import fields, models, api
from datetime import datetime, timedelta


class Period(models.Model):
    _name = 'school.period'
    _description = 'Periods'
    _rec_name = 'course_id'

    start_time = fields.Datetime(string='Period Start Time', required=True
                                 , default=datetime.now())
    end_time = fields.Datetime(string='Period End Time', required=True
                               , default=datetime.now())
    duration = fields.Char(compute='_period_duration',
                           string='Duration of Period', required=True)
    location = fields.Char('Class-Room', required=True, size=10)
    course_id = fields.Many2one('school.course', string="Course",
                                ondelete='cascade')
    teacher_id = fields.Many2one(related='course_id.teacher_id',
                                 string="Teacher")

    @api.depends('start_time', 'end_time')
    def _period_duration(self):
        for per in self:
            period = per.end_time - per.start_time
            per.duration = timedelta(seconds=period.seconds)
