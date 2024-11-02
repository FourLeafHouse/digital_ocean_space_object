from odoo import fields, models, api
from odoo.addons.digital_ocean_space_object.utils import DigitalOcean

class Folder(models.Model):
    _name = 'do.folder'
    _description = 'DO Folder'
    _rec_name = 'path'

    name = fields.Char('Folder Name')
    parent_folder = fields.Many2one('do.folder')
    space_id = fields.Many2one('do.space.object',ondelete='restrict')
    path = fields.Char('Path')
    state = fields.Selection([
        ('draft','Draft'),
        ('created','created'),
        ('deleted','deleted'),
    ],default="draft")

    @api.constrains("name", "parent_folder")
    def folder_path(self):
        for res in self:
            path = ''
            if res.parent_folder:
                path += res.parent_folder.name + '/'
            path += res.name + '/'
            res.path = path

    def action_create(self):
        self.s3().create_folder(self.path)
        self.state = 'created'

    def action_delete(self):
        if self.path: self.s3().delete_folder(self.path)
        self.state = 'deleted'

    def action_reset(self):
        self.state = 'draft'

    def unlink(self):
        for record in self:
            if record.state == 'created':
                if record.path: record.s3().delete(record.path)
        return super().unlink()

    def s3(self):
        return DigitalOcean(self.env['ir.config_parameter'].sudo(),self.space_id.region,self.space_id.name)