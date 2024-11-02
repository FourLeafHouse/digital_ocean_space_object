from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.addons.digital_ocean_space_object.utils import DigitalOcean

class Upload(models.Model):
    _name = "do.upload"
    _description = "Upload Data"

    name = fields.Char('Name')
    upload_data = fields.Binary('Upload')
    type = fields.Selection([
        ('private', 'Private'),
        ('public', 'Public'),
    ], default="private")
    folder_path = fields.Many2one('do.folder')
    full_path = fields.Char()
    url = fields.Char()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('created', 'created'),
        ('deleted', 'deleted'),
    ], default="draft")
    remove_binary = fields.Boolean('Upload After Delete Video Binary',default=False)

    @api.constrains("name","upload_data","folder_path")
    def space_folder_path(self):
        for res in self:
            path = ''
            if res.folder_path:
                path += res.folder_path.name + '/'
            path += res.name
            res.full_path = path
        return True

    def action_create(self):
        url = self.s3().upload(upload_data=self.upload_data,upload_path=self.full_path,type=self.type)
        self.url = url
        if self.url and self.remove_binary:
            self.upload_data = False
        self.state = 'created'


    def action_delete(self):
        if self.full_path: self.s3().delete(self.full_path)
        self.url = ''
        self.state = 'deleted'

    def action_download(self):
        self.s3().download(self.full_path,self.name)

    def action_reset(self):
        self.state = 'draft'

    def unlink(self):
        for record in self:
            if record.state == 'created':
                if record.full_path: record.s3().delete(record.full_path)
        return super().unlink()

    def s3(self):
        return DigitalOcean(self.env['ir.config_parameter'].sudo(), self.folder_path.space_id.region, self.folder_path.space_id.name)