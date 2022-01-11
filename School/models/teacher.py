from odoo import fields, models, api


class Teacher(models.Model):
    _name = 'school.teacher'
    _description = 'Teacher'
    _inherits = {'res.partner': 'teacher_id'}

    teacher_id = fields.Many2one('res.partner', string='Teacher-ID',
                                 required=True)
    school_id = fields.Many2one('res.company', string='School',
                                required=True)
    course_ids = fields.One2many('school.course', 'teacher_id',
                                 string='Courses')
    period_ids = fields.One2many(related='course_ids.schedule',
                                 string='Schedule')
    language = fields.Many2many('res.lang', string='Languages')
    country_id = fields.Many2one('res.country', string='Country Name',
                                 required=True)
    teacher_signature = fields.Binary(string='Signature')

    @api.model
    def create(self, values):
        values['name'] = 'Lecturer ' + values['name']
        rtn = super(Teacher, self).create(values)
        return rtn
