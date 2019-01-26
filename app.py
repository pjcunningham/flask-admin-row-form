from flask import Flask
from flask_admin import Admin
from models import db, Student
from commands import create_database

app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
db.init_app(app)

app.cli.add_command(create_database)


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


from views import StudentView

admin = Admin(app, template_mode="bootstrap3")
admin.add_view(StudentView(Student, db.session))


if __name__ == '__main__':
    app.run()
