import os


def s_key(app):
    app.secret_key = os.urandom(36)
    # app.secret_key = 'zxczxc'
    # print(app.secret_key)
