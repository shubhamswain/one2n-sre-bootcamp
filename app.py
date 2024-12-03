from flask import Flask, request, got_request_exception
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


def log_exception(sender, exception, **extra):
    """ Log an exception to our logging framework """
    sender.logger.debug('Got exception during processing: %s', exception)


app = Flask(__name__)
api = Api(app, catch_all_404s=True)

got_request_exception.connect(log_exception, app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

studentFields = {
    'id':fields.Integer,
    'first_name':fields.String,
    'last_name':fields.String,
    'age':fields.Integer
 }

class StudentDB(db.Model):
    # Id : Field which stores unique id for every row in 
    # database table.
    # first_name: Used to store the first name if the user
    # last_name: Used to store last name of the user
    # Age: Used to store the age of the user
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"ID : {self.id}, Name : {self.first_name} {self.last_name}, Age: {self.age}"
    

def abort_if_student_doesnt_exist(pk):
    db.session.query(User.id).filter_by(name='davidism').first() is not None
    if pk not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

class Student(Resource):
    @marshal_with(studentFields)
    def get(self, pk):
        student = StudentDB.query.filter_by(id=pk).first()
        return student
    
    @marshal_with(studentFields)
    def put(self, pk):
        data = request.json
        student = StudentDB.query.filter_by(id=pk).first()
        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.age = data['age']
        db.session.commit()
        return student
    
    @marshal_with(studentFields)
    def delete(self, pk):
        student = StudentDB.query.filter_by(id=pk).first()
        db.session.delete(student)
        db.session.commit()
        all_students = StudentDB.query.all()
        return all_students


class Students(Resource):
    @marshal_with(studentFields)
    def get(self):
        all_students = StudentDB.query.all()
        return all_students
    
    @marshal_with(studentFields)
    def post(self):
        data = request.json
        student = StudentDB(first_name=data['first_name'], last_name=data['last_name'], age=data['age'])
        db.session.add(student)
        db.session.commit()
        return student

api.add_resource(Students, '/api/v1/students')
api.add_resource(Student, '/api/v1/student/<int:pk>')

if __name__ == '__main__':
    app.run(debug=True)