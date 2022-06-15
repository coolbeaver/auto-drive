
def save_image(file, app, secure_filename, os, randint, path):
    if str(file.filename):
        UPLOAD_FOLDER = path
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        file.filename = f'{randint(1, 999999999999)}.jpg'
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filename = f'/{path}{filename}'
    else:
        filename = None

    return filename
