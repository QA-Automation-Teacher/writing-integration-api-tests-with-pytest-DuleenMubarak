import requests
import json

BASE_URL = "http://localhost:5000"

# Test GET

def test_get_posts():
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code in [200,201]
    assert isinstance(response.json(), list)

def test_get_post_by_id_invalid_id():
    post_id = "invalid_id"
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 500

def test_get_post_by_id_non_integer():
    post_id = "abc"
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 500

def test_get_rate_limiting():
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    for _ in range(10):  
        response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code ==200


def test_get_post_by_id():
    post_id = 20
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code in [200,201]
    assert isinstance(response.json(), dict)
    assert int(response.json().get('id')) == post_id

def test_get_nonexistent_post():
    post_id = 10000
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code not in [200,201]



# Test POST

def test_create_post():
    new_post = {
        "userId": 9,
        "title": "New Post Title",
        "body": "This is the body of the new post"
    }
    response = requests.post(f"{BASE_URL}/posts", json=new_post)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["userId"] == new_post["userId"]
    assert response_data["title"] == new_post["title"]
    assert response_data["body"] == new_post["body"]

def test_create_post_missing_data():
    incomplete_post = {
        "userId": 9,
        "title": "Post with missing body"
    }
    response = requests.post(f"{BASE_URL}/posts", json=incomplete_post)
    assert response.status_code in [200,201,202,203,204,205]


def test_create_post_with_extra_fields():
    new_post = {
        "userId": 9,
        "title": "Post with extra fields",
        "body": "This post includes unexpected fields.",
        "extra_field": "Unexpected data",
    }
    response = requests.post(f"{BASE_URL}/posts", json=new_post)
    assert response.status_code in [200,201,202,203,204,205]
    response_data = response.json()
    assert "extra_field" in response_data


def test_create_post_with_null_fields():
    new_post = {
        "userId": None,
        "title": None,
        "body": None
    }
    response = requests.post(f"{BASE_URL}/posts", json=new_post)
    assert response.status_code in [200,201]

def test_create_post_empty_payload():
    response = requests.post(f"{BASE_URL}/posts", json={})
    assert response.status_code == 400

def test_create_post_non_json_payload():
    response = requests.post(f"{BASE_URL}/posts", data="Non-JSON payload")
    assert response.status_code == 415


# Test PATCH

def test_patch_update_post():
    post_id = 20
    update_data = {
        "title": "Updated Post Title",
        "body": "Updated post body content"
    }
    response = requests.patch(f"{BASE_URL}/posts/{post_id}", json=update_data)
    assert response.status_code in [200,201,202,203,204,205]
    response_data = response.json()
    assert response_data["title"] == update_data["title"]
    assert response_data["body"] == update_data["body"]

def test_patch_post_with_empty_payload():
    post_id = 1
    response = requests.patch(f"{BASE_URL}/posts/{post_id}", json={})
    assert response.status_code == 400


def test_patch_partial_update_invalid_post():
    post_id = 9999 
    update_data = {
        "title": "Nonexistent post update"
    }
    response = requests.patch(f"{BASE_URL}/posts/{post_id}", json=update_data)
    assert response.status_code == 404
    
def test_patch_update_nonexistent_post():
    post_id = 9999
    update_data = {
        "title": "Nonexistent Post",
        "body": "Trying to update a non-existent post"
    }
    response = requests.patch(f"{BASE_URL}/posts/{post_id}", json=update_data)
    assert response.status_code == 404


def test_patch_post_invalid_field():
    post_id = 1
    updated_data = {"invalid_field": "Invalid data"}
    response = requests.patch(f"{BASE_URL}/posts/{post_id}", json=updated_data)
    assert response.status_code == 404

# Test DELETE 

def test_delete_post():
    post_id = 30
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "success"
    assert response_data["message"] == "Post deleted"

def test_delete_nonexistent_post():
    post_id = 9999
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200


def test_delete_post_numeric_string_id():
    post_id = "60"
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200

def test_delete_post_empty_id():
    post_id = ""
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 404 



