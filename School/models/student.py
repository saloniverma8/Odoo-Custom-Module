from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Student(models.Model):
    _name = 'school.student'
    _description = 'Student'
    _inherits = {'res.partner': 'partner_id'}
    partner_id = fields.Many2one('res.partner', required=True,
                                 ondelete='restrict', auto_join=True,
                                 string='Related Partner',
                                 help='Partner-related data of the student')
    identity_number = fields.Char(string='Identification number', required=True,
                                  size=10)
    school_id = fields.Many2one('res.company', string='School-ID',
                                required=True,
                                default=lambda self: self.env.company)
    course_id = fields.Many2many('school.course', string='Course')
    schedule = fields.One2many(related='course_id.schedule',
                               string='Student Schedule', readonly=True)
    student_signature = fields.Binary(string='Signature')
    note = fields.Text(string='Note')

    _sql_constraints = [('id_uniq', 'unique(identity_number)',
                         'The identification number must be unique..!!!')]

    @api.constrains('mobile')
    def check_identity_number(self):
        for rec in self:
            if len(rec.mobile) < 12:
                raise ValidationError('Incorrect Mobile Number!')
