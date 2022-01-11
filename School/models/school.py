from odoo import fields, models

"""
This is the Language School module.

"""


class School(models.Model):
    _inherit = 'res.company'

    school_identity_number = fields.Char(string='Identification number'
                                         , size=10)
    school_type = fields.Selection([('public', 'Public_School'),
                                    ('private', 'Private_School')]
                                   , string='Type Of School')
