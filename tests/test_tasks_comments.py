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


def test_tasks_comments_flow(client):
    user_email = f"user_{uuid.uuid4().hex[:6]}@example.com"
    author_email = f"author_{uuid.uuid4().hex[:6]}@example.com"

    user_token = register_and_login(client, user_email, "user")
    author_token = register_and_login(client, author_email, "author")

    # user creates task
    res = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"description": "Task", "comment": "Initial comment"},
    )
    assert res.status_code == 201
    task = res.json()
    task_id = task["id"]

    # author cannot create task
    res = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {author_token}"},
        json={"description": "Task", "comment": "Nope"},
    )
    assert res.status_code == 403

    # author creates comment
    res = client.post(
        "/comments/",
        headers={"Authorization": f"Bearer {author_token}"},
        json={"text": "Looks good", "task_id": task_id},
    )
    assert res.status_code == 201
    comment_id = res.json()["id"]

    # user cannot create comment
    res = client.post(
        "/comments/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"text": "Nope", "task_id": task_id},
    )
    assert res.status_code == 403

    # list comments for task
    res = client.get(
        f"/comments/?task_id={task_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert res.status_code == 200

    # cleanup
    res = client.delete(
        f"/comments/{comment_id}",
        headers={"Authorization": f"Bearer {author_token}"},
    )
    assert res.status_code == 204

    res = client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert res.status_code == 204
