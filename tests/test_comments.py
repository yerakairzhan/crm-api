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


def create_task(client, token):
    res = client.post(
        "/tasks/",
        headers=auth_headers(token),
        json={"description": "Task", "comment": "Init"},
    )
    assert res.status_code == 201
    return res.json()["id"]


def test_comment_requires_author_role(client):
    user_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    user_token = register_and_login(client, user_email, "user")

    task_id = create_task(client, user_token)

    res = client.post(
        "/comments/",
        headers=auth_headers(user_token),
        json={"text": "Nope", "task_id": task_id},
    )
    assert res.status_code == 403


def test_comment_owner_only_update_delete(client):
    user_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    author1_email = f"author_{uuid.uuid4().hex[:8]}@example.com"
    author2_email = f"author_{uuid.uuid4().hex[:8]}@example.com"

    user_token = register_and_login(client, user_email, "user")
    author1_token = register_and_login(client, author1_email, "author")
    author2_token = register_and_login(client, author2_email, "author")

    task_id = create_task(client, user_token)

    res = client.post(
        "/comments/",
        headers=auth_headers(author1_token),
        json={"text": "Looks good", "task_id": task_id},
    )
    assert res.status_code == 201
    comment_id = res.json()["id"]

    res = client.patch(
        f"/comments/{comment_id}",
        headers=auth_headers(author2_token),
        json={"text": "Hack"},
    )
    assert res.status_code == 403

    res = client.delete(
        f"/comments/{comment_id}",
        headers=auth_headers(author2_token),
    )
    assert res.status_code == 403

    res = client.patch(
        f"/comments/{comment_id}",
        headers=auth_headers(author1_token),
        json={"text": "Updated"},
    )
    assert res.status_code == 200

    res = client.delete(
        f"/comments/{comment_id}",
        headers=auth_headers(author1_token),
    )
    assert res.status_code == 204


def test_comment_filter_by_task(client):
    user_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    author_email = f"author_{uuid.uuid4().hex[:8]}@example.com"

    user_token = register_and_login(client, user_email, "user")
    author_token = register_and_login(client, author_email, "author")

    task_a = create_task(client, user_token)
    task_b = create_task(client, user_token)

    res = client.post(
        "/comments/",
        headers=auth_headers(author_token),
        json={"text": "A1", "task_id": task_a},
    )
    assert res.status_code == 201

    res = client.post(
        "/comments/",
        headers=auth_headers(author_token),
        json={"text": "B1", "task_id": task_b},
    )
    assert res.status_code == 201

    res = client.get(
        f"/comments/?task_id={task_a}",
        headers=auth_headers(user_token),
    )
    assert res.status_code == 200
    data = res.json()
    assert all(item["task_id"] == task_a for item in data)


def test_comments_require_auth(client):
    res = client.get("/comments/")
    assert res.status_code in (401, 403)

    res = client.post("/comments/", json={"text": "x", "task_id": str(uuid.uuid4())})
    assert res.status_code in (401, 403)
