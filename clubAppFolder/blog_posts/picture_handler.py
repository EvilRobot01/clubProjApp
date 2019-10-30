import os 
from PIL import Image
from flask import url_for, current_app

def add_blog_image(image_upload, blogtitle):

    filename = image_upload.filename
    ext_type = filename.split('.')[-1]
    storage_filename = str(blogtitle)+'.'+ext_type

    filepath = os.path.join(current_app.root_path, 'static\blog_images', storage_filename)

    output_size = (200, 200)

    pic = Image.open(image_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename