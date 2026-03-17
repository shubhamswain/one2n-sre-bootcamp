from flask import Flask, request, got_request_exception, abort
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging

def log_exception(sender, exception, **extra):
    sender.logger.error(f'Exception during request: {exception}', exc_info=True)

app = Flask(__name__)

# Configure logging (optional: adjust level and format as needed)
logging.basicConfig(
    filename='logs/app.log',  # Logs will be written to 'app.log' in the project root
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@app.before_request
def log_request_info():
    app.logger.info(
        (
            f'Request: {request.method} {request.url} - '
            f'Data: {request.get_json(silent=True)}'
        )
    )

@app.after_request
def log_response_info(response):
    app.logger.info(
        f'Response: {response.status_code} - Data: {response.get_json(silent=True)}'
    )
    return response

api = Api(app, catch_all_404s=True)

got_request_exception.connect(log_exception, app)

app.config.from_pyfile('settings.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

studentFields = {
    'id':fields.Integer,
    'first_name':fields.String,
    'last_name':fields.String,
    'age':fields.Integer,
    'grade':fields.String
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
    grade = db.Column(db.String(2), unique=False)

    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return (
            f"ID : {self.id}, Name : {self.first_name} {self.last_name}, "
            f"Age: {self.age}, Grade: {self.grade}"
        )
    


class Student(Resource):
    @marshal_with(studentFields)
    def get(self, pk):
        student = db.session.get(StudentDB, pk)
        if student is None:
            abort(404, description="Student with the specified ID does not exist.")
        return student

    @marshal_with(studentFields)
    def put(self, pk):
        data = request.json
        student = db.session.get(StudentDB, pk)
        if student is None:
            abort(404, description="Student with the specified ID does not exist.")
        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.age = data['age']
        student.grade = data['grade']
        db.session.commit()
        app.logger.info(f'Updated student: {student.id}')
        return student
    
    @marshal_with(studentFields)
    def delete(self, pk):
        student = db.session.get(StudentDB, pk)
        if student is None:
            abort(404, description="Student with the specified ID does not exist.")
        db.session.delete(student)
        db.session.commit()
        all_students = StudentDB.query.all()
        app.logger.info(f'Deleted student: {student.id}')
        return all_students


class Students(Resource):
    @marshal_with(studentFields)
    def get(self):
        all_students = StudentDB.query.all()
        return all_students
    
    @marshal_with(studentFields)
    def post(self):
        data = request.json
        if not data:
            abort(400, description="No input data provided")
        try:
            student = StudentDB(
                first_name=data['first_name'],
                last_name=data['last_name'],
                age=data['age'],
                grade=data['grade']
            )
        except KeyError as e:
            abort(400, description=f"Missing required field: {e.args[0]}")
        db.session.add(student)
        db.session.commit()
        app.logger.info(f'Created student: {student.id}')
        return student

class HealthCheck(Resource):
    def get(self):
        try:
            # Simple DB query to check connectivity
            db.session.execute(db.text('SELECT 1'))
            return {"status": "healthy", "database": "connected"}
        except Exception as e:
            app.logger.error(f'Error occurred: {e}')
            return {
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }, 500

api.add_resource(HealthCheck, '/api/v1/healthcheck')
api.add_resource(Students, '/api/v1/students')
api.add_resource(Student, '/api/v1/students/<int:pk>')

if __name__ == '__main__':
    app.run(debug=True)