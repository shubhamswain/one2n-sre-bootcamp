import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
from app import app, db  # Adjust imports as needed # noqa: E402

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables
            yield client
            db.drop_all()  # Clean up after tests

def test_healthcheck(client):
    response = client.get('/api/v1/healthcheck')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'database' in data

def test_get_students_empty(client):
    response = client.get('/api/v1/students')
    assert response.status_code == 200
    assert response.get_json() == []

def test_post_student(client):
    data = {'first_name': 'John', 'last_name': 'Doe', 'age': 20, 'grade': 'A'}
    response = client.post('/api/v1/students', json=data)
    assert response.status_code == 200
    student = response.get_json()
    assert student['first_name'] == 'John'
    assert 'id' in student

def test_get_students_after_post(client):
    # First, post a student
    data = {'first_name': 'Jane', 'last_name': 'Smith', 'age': 22, 'grade': 'B'}
    client.post('/api/v1/students', json=data)
    
    response = client.get('/api/v1/students')
    assert response.status_code == 200
    students = response.get_json()
    assert len(students) == 1
    assert students[0]['first_name'] == 'Jane'

def test_get_student(client):
    # Create a student first
    data = {'first_name': 'Alice', 'last_name': 'Wonder', 'age': 19, 'grade': 'A'}
    post_response = client.post('/api/v1/students', json=data)
    student_id = post_response.get_json()['id']
    
    response = client.get(f'/api/v1/students/{student_id}')
    assert response.status_code == 200
    student = response.get_json()
    assert student['first_name'] == 'Alice'

def test_get_student_not_found(client):
    response = client.get('/api/v1/students/999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'message' in data  # Assuming custom 404 message

def test_put_student(client):
    # Create and update
    data = {'first_name': 'Bob', 'last_name': 'Builder', 'age': 21, 'grade': 'C'}
    post_response = client.post('/api/v1/students', json=data)
    student_id = post_response.get_json()['id']
    
    update_data = {'first_name': 'Bob', 'last_name': 'Builder', 'age': 22, 'grade': 'B'}
    response = client.put(f'/api/v1/students/{student_id}', json=update_data)
    assert response.status_code == 200
    student = response.get_json()
    assert student['age'] == 22

def test_delete_student(client):
    # Create and delete
    data = {'first_name': 'Charlie', 'last_name': 'Brown', 'age': 18, 'grade': 'D'}
    post_response = client.post('/api/v1/students', json=data)
    student_id = post_response.get_json()['id']
    
    response = client.delete(f'/api/v1/students/{student_id}')
    assert response.status_code == 200
    # Verify deletion by checking the returned list or a new GET
    get_response = client.get('/api/v1/students')
    students = get_response.get_json()
    assert len(students) == 0  # Assuming no other students