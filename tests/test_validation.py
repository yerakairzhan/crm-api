import uuid


def register_and_login(client, email, role):
    res = client.post(
        "/auth/register",
        json={"email": email, "password": "password123", "role": role},
    )
    assert res.status_code == 201
    res = client.post(
        "/auth/login",
        json={"email": email, "password": "password123"},
    )
    assert res.status_code == 200
    return res.json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_user_password_min_length(client, unique_email):
    res = client.post(
        "/auth/register",
        json={"email": unique_email, "password": "123", "role": "user"},
    )
    assert res.status_code == 422


def test_task_validation_required_fields(client):
    user_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    token = register_and_login(client, user_email, "user")

    res = client.post(
        "/tasks/",
        headers=auth_headers(token),
        json={"description": "", "comment": "x"},
    )
    assert res.status_code == 422

    res = client.post(
        "/tasks/",
        headers=auth_headers(token),
        json={"description": "x", "comment": ""},
    )
    assert res.status_code == 422


def test_comment_validation_required_fields(client):
    user_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    author_email = f"author_{uuid.uuid4().hex[:8]}@example.com"

    user_token = register_and_login(client, user_email, "user")
    author_token = register_and_login(client, author_email, "author")

    res = client.post(
        "/tasks/",
        headers=auth_headers(user_token),
        json={"description": "Task", "comment": "Init"},
    )
    assert res.status_code == 201
    task_id = res.json()["id"]

    res = client.post(
        "/comments/",
        headers=auth_headers(author_token),
        json={"text": "", "task_id": task_id},
    )
    assert res.status_code == 422

    res = client.post(
        "/comments/",
        headers=auth_headers(author_token),
        json={"text": "ok", "task_id": "not-a-uuid"},
    )
    assert res.status_code == 422
