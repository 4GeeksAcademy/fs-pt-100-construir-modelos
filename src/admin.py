import os
from flask_admin import Admin
from models import db, Users, Profiles, Enrollments, Students, Teachers
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(Profiles, db.session))
    admin.add_view(ModelView(Students, db.session))
    admin.add_view(ModelView(Teachers, db.session))
    admin.add_view(ModelView(Enrollments, db.session))
    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))