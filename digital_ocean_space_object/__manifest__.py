{
    "name": "Digital Ocean Space Object",
    "summary": "Digital Ocean Space Integration with Odoo Folder/File CRUD",
    "version": "17.0.1.0.0",
    "category": "Extra Tools",
    "author": "WaiYan-DEVJ@K3R, FourLeafHouse",
    "license": "LGPL-3",
    "external_dependencies": {
            "python": ["boto3"],
        },
    "depends": ['base'],
    "data": [
            "security/ir.model.access.csv",
            "views/setting_config_view.xml",
            "views/space_object_view.xml",
            "views/folder_view.xml",
            "views/upload_view.xml"
        ],
    "images": ['static/description/banner.png'],
    "application": True,
    "installable": True,
    "auto_install": False
}