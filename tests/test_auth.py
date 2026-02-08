def test_register_login_refresh(client, unique_email):
    # register user
    res = client.post(
        "/auth/register",
        json={"email": unique_email, "password": "password123", "role": "user"},
    )
    assert res.status_code == 201
    user = res.json()
    assert user["email"] == unique_email

    # login
    res = client.post(
        "/auth/login",
        json={"email": unique_email, "password": "password123"},
    )
    assert res.status_code == 200
    tokens = res.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

    # refresh
    res = client.post("/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert res.status_code == 200
    refreshed = res.json()
    assert "access_token" in refreshed
    assert "refresh_token" in refreshed
