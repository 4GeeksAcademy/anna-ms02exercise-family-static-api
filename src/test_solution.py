import pytest
import json
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_all_members(client):
    response = client.get('/members')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert type(data) is list

def test_get_single_member(client):
    response = client.get('/member/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['first_name'] == 'John'

def test_add_member(client):
    new_member = {
        "first_name": "Tommy",
        "age": 23,
        "lucky_numbers": [34, 65, 23, 4, 6]
    }
    response = client.post('/member', json=new_member)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['first_name'] == 'Tommy'

def test_delete_member(client):
    response = client.delete('/member/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['done'] == True