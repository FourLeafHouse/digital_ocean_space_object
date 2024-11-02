import os

import boto3
from odoo.exceptions import ValidationError

class DigitalOcean:
    def __init__(self, ir_config_parameter,region,space_name):
        self.parm = ir_config_parameter
        self.region = region
        self.space_name = space_name
        self.validate_config()

    def try_decorator(name):
        def exp_validate (func):
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    raise ValidationError(f"An exception occurred: {e} - {name}")

            return wrapper
        return exp_validate

    def validate_config(self):
        if not self.parm.get_param('access_key'):
            raise ValidationError(f"Digital Ocean Setting access key not fond.")
        if not self.parm.get_param('secret_key'):
            raise ValidationError(f"Digital Ocean Setting secret key not fond.")

    def file_path_check(self,file_path):
        s3 = self.space_connection()
        response = s3.list_objects_v2(Bucket=self.space_name, Prefix=file_path)
        if 'Contents' not in response:
            raise ValidationError(f"Path {file_path} not found.")

    @try_decorator('Space Connection')
    def space_connection(self):
        session = boto3.session.Session()
        s3 = session.client(
            's3',
            region_name=self.region,
            endpoint_url=f'https://{self.region}.digitaloceanspaces.com',
            aws_access_key_id=self.parm.get_param('access_key'),
            aws_secret_access_key=self.parm.get_param('secret_key'),
        )
        return s3

    @try_decorator('Create Folder')
    def create_folder(self,space_path):
        # try:
            s3 = self.space_connection()
            response = s3.list_objects_v2(Bucket=self.space_name, Prefix=space_path)
            if 'Contents' in response:
                objects = [{'Key': obj['Key']} for obj in response['Contents']]
                print(objects)
                raise ValidationError(f"Already created folder.\n"
                                      f"Folder Path : {space_path}")
            s3.put_object(Bucket=self.space_name, Key=space_path)
        # except Exception as e:
        #     raise ValidationError(f"{e} -- Create Folder")

    @try_decorator('Delete Folder')
    def delete_folder(self,space_path):
        s3 = self.space_connection()
        response = s3.list_objects_v2(Bucket=self.space_name, Prefix=space_path)
        # If objects are found, delete them
        if 'Contents' in response:
            objects = [{'Key': obj['Key']} for obj in response['Contents']]
            s3.delete_objects(Bucket=self.space_name, Delete={'Objects': objects})
        else:
            raise ValidationError(f"Path {space_path} not found.")


    @try_decorator('upload')
    def upload(self,upload_data,upload_path,type='private'):
        s3 = self.space_connection()
        file_path = upload_data
        # Specify the key under which you want to store the file in your Space
        object_key = upload_path
        # Upload the file to your Space
        # with open(file_path, 'rb') as file:
        if type == 'private':
            # For private
            s3.put_object(Bucket=self.space_name, Key=object_key, Body=file_path)
        else:
            # For Public
            s3.put_object(Bucket=self.space_name, Key=object_key, Body=file_path, ACL="public-read")


        return f"https://{self.space_name}.{self.region}.digitaloceanspaces.com/{object_key}"

    @try_decorator('Delete')
    def delete(self,delete_path):
        s3 = self.space_connection()
        file_path = delete_path
        response = s3.list_objects_v2(Bucket=self.space_name, Prefix=delete_path)
        # If objects are found, delete them
        if 'Contents' in response:
            objects = [{'Key': obj['Key']} for obj in response['Contents']]
            s3.delete_object(Bucket=self.space_name, Key=file_path)
        else:
            raise ValidationError(f"Path {delete_path} not found.")

    @try_decorator('Download')
    def download(self, download_path,file_name):
        s3 = self.space_connection()
        file_path = download_path
        self.file_path_check(file_path)
        s3.download_file(self.space_name, download_path, file_name)
        response = s3.get_object(Bucket=self.space_name, Key=download_path)
        receive_path = '/digital_ocean_space_object/'+file_name # Change Custom file Path
        with open(receive_path, 'wb') as file:
            file.write(response['Body'].read())



