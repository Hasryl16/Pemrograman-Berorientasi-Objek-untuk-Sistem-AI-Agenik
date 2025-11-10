import pytest
from api import app, krs, machine, KRSStatus
from models import Course
from hypothesis import given, settings, strategies as st

course_strategy = st.fixed_dictionaries({
    "nama": st.text(min_size=1, max_size=10),
    "sks": st.integers(min_value=1, max_value=4)
})

def total_sks(courses):
    return sum(course["sks"] for course in courses)

@settings(max_examples=1000)
@given(st.lists(course_strategy, min_size=0, max_size=6))
def test_total_sks_never_exceeds_limit(courses):
    total = total_sks(courses)
    assert total <= 24, f"Total SKS {total} melebihi batas maksimum 24!"

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def reset_state():
    # Reset KRS and machine state before each test
    krs.courses.clear()
    machine.state = KRSStatus.DRAFT

def test_get_krs(client):
    response = client.get('/krs')
    assert response.status_code == 200
    data = response.get_json()
    assert 'nim' in data
    assert 'status' in data
    assert 'courses' in data
    assert 'total_sks' in data

def test_add_course_success(client):
    course_data = {
        "nama": "Matematika Lanjutan",
        "sks": 3,
        "jadwal": "Senin 08:00",
        "prasyarat": ["Matematika Dasar"]
    }
    response = client.post('/krs/add', json=course_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert len(krs.courses) == 1

def test_add_course_validation_fail(client):
    # Add a course that exceeds SKS limit
    for i in range(10):
        course_data = {
            "nama": f"Course {i}",
            "sks": 4,
            "jadwal": f"Day {i}",
            "prasyarat": []
        }
        client.post('/krs/add', json=course_data)
    # Try to add one more
    course_data = {
        "nama": "Extra Course",
        "sks": 4,
        "jadwal": "Extra Day",
        "prasyarat": []
    }
    response = client.post('/krs/add', json=course_data)
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] == False

def test_remove_course_success(client):
    # First add a course
    course_data = {
        "nama": "Matematika Lanjutan",
        "sks": 3,
        "jadwal": "Senin 08:00",
        "prasyarat": ["Matematika Dasar"]
    }
    client.post('/krs/add', json=course_data)
    # Now remove it
    response = client.delete('/krs/remove', json={"nama": "Matematika Lanjutan"})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert len(krs.courses) == 0

def test_remove_course_not_found(client):
    response = client.delete('/krs/remove', json={"nama": "Nonexistent Course"})
    assert response.status_code == 404
    data = response.get_json()
    assert data['success'] == False

def test_submit_krs_success(client):
    # Add a valid course
    course_data = {
        "nama": "Matematika Lanjutan",
        "sks": 3,
        "jadwal": "Senin 08:00",
        "prasyarat": ["Matematika Dasar"]
    }
    client.post('/krs/add', json=course_data)
    response = client.post('/krs/submit')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert machine.state == KRSStatus.SUBMITTED

def test_submit_krs_fail(client):
    # Try to submit with prerequisite not met
    course_data = {
        "nama": "Matematika Lanjutan",
        "sks": 3,
        "jadwal": "Senin 08:00",
        "prasyarat": ["Kalkulus"]
    }
    response = client.post('/krs/add', json=course_data)
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] == False

def test_revise_krs(client):
    # First submit
    course_data = {
        "nama": "Matematika Lanjutan",
        "sks": 3,
        "jadwal": "Senin 08:00",
        "prasyarat": ["Matematika Dasar"]
    }
    client.post('/krs/add', json=course_data)
    client.post('/krs/submit')
    # Now revise
    response = client.post('/krs/revision')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert machine.state == KRSStatus.REVISION

def test_approve_krs(client):
    # First submit
    course_data = {
        "nama": "Matematika Lanjutan",
        "sks": 3,
        "jadwal": "Senin 08:00",
        "prasyarat": ["Matematika Dasar"]
    }
    client.post('/krs/add', json=course_data)
    client.post('/krs/submit')
    # Now approve directly from SUBMITTED
    response = client.post('/krs/approve')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert machine.state == KRSStatus.APPROVED
