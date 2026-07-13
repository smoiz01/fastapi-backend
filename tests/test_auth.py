def test_login(client, test_user):
    res = client.post("/login", 
        data = {
            "username": test_user["email"],
            "password": test_user["password"]
        } )

    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["access_token"] 
    assert data["token_type"] == "bearer"
    assert "password" not in data

def test_login_password_exception(client, test_user):
    res = client.post("/login", 
        data = {
            "username": test_user["email"],
            "password": "qwerd123"
        } )
    
    assert res.status_code == 403
    assert res.json().get("detail") == "invalid credentials"
    assert "access_token" not in res.json()

def test_login_email_exception(client, test_user):
    res = client.post("/login", 
        data = {
            "username": "test_user@abc.com",
            "password": test_user["password"]
        } )
    
    assert res.status_code == 403
    assert res.json().get("detail") == "invalid credentials"
    assert "access_token" not in res.json()
    
    