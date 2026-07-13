def test_vote(authorized_client, test_post):
    post_id = test_post["id"]
    res = authorized_client.post("/vote/", json = {"post_id": post_id, "dir": 1})

    assert res.status_code == 201

def test_vote_post_not_found(authorized_client):
    res = authorized_client.post(f"/vote/", json = {"post_id": 999999, "dir": 1})

    assert res.status_code == 404
    assert 'not found' in res.json()['detail']

def test_vote_already_voted(authorized_client, test_post):
    post_id = test_post["id"]
    res = authorized_client.post("/vote/", json = {"post_id": post_id, "dir": 1})
    res1 = authorized_client.post("/vote/", json = {"post_id": post_id, "dir": 1})

    assert res.status_code == 201
    assert res1.status_code == 409
    assert "already voted" in res1.json()['detail']

def test_vote_down(authorized_client, test_post):
    post_id = test_post["id"]
    res = authorized_client.post("/vote/", json = {"post_id": post_id, "dir": 1})
    res1 = authorized_client.post("/vote/", json = {"post_id": post_id, "dir": 0})

    assert res.status_code == 201
    assert res1.status_code == 201
    assert res1.json()['message'] == "successfully deleted vote" 

def test_vote_down_not_voted(authorized_client, test_post):
    post_id = test_post["id"]
    res1 = authorized_client.post("/vote/", json = {"post_id": post_id, "dir": 0})

    assert res1.status_code == 404
    assert "has not voted" in res1.json()['detail']


