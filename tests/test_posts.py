def test_get_all_posts(authorized_client):
    res = authorized_client.get(f"/posts/")

    assert res.status_code == 200

def test_get_post(authorized_client, test_post):
    post_id = test_post['id']
    res = authorized_client.get(f"/posts/{post_id}")

    data = res.json()
    assert res.status_code == 200
    assert "title" in data
    assert "content" in data
    assert data["published"] == True
    assert "votes" in data
    assert "user_id" in data

def test_get_post_not_found(authorized_client):
    res = authorized_client.get(f"/posts/99999")

    assert res.status_code == 404
    assert "was not found" in res.json()['detail']

def test_get_post_unauthorized(client, test_post):
    post_id = test_post['id']
    res = client.get(f"/posts/{post_id}")

    assert res.status_code == 401

def test_create_post(authorized_client):
    res = authorized_client.post("/posts/", json = {
        "title": "My first post",
        "content": "Hello world",
        })
    
    data = res.json()
    assert res.status_code == 201
    assert "title" in data
    assert "content" in data
    assert data["published"] == True

def test_create_post_unauthorized(client):
    res = client.post("/posts/", json = {
        "title": "My first post",
        "content": "Hello world",
        })
    
    assert res.status_code == 401

def test_post_delete(authorized_client, test_post):
    post_id = test_post['id']
    res = authorized_client.delete(f"/posts/{post_id}")

    assert res.status_code == 204

def test_post_delete_not_found(authorized_client):
    res = authorized_client.delete(f"/posts/999999")

    assert res.status_code == 404
    assert "was not found" in res.json()['detail']

def test_post_delete_forbidden(authorized_client_2, test_post):
    post_id = test_post['id']
    res = authorized_client_2.delete(f"/posts/{post_id}")

    assert res.status_code == 403
    assert "not authorized" in res.json()["detail"]

def test_post_update(authorized_client, test_post):
    post_id = test_post['id']
    res = authorized_client.put(f"/posts/{post_id}", json = {
        "title": "update post",
        "content": "updated post",
        })

    data = res.json()

    assert res.status_code == 202
    assert data["title"] == "update post"
    assert data["content"] == "updated post"
    
def test_post_update_not_found(authorized_client):
    res = authorized_client.put(f"/posts/999999", json = {
        "title": "update post",
        "content": "updated post",
        })

    assert res.status_code == 404
    assert "was not found" in res.json()['detail']

def test_post_update_forbidden(authorized_client_2, test_post):
    post_id = test_post['id']
    res = authorized_client_2.put(f"/posts/{post_id}", json = {
        "title": "update post",
        "content": "updated post",
        })

    assert res.status_code == 403
    assert "not authorized" in res.json()["detail"]