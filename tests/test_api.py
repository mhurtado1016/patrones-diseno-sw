import pytest


def test_login_ok_and_token_works(client):
    r = client.post("/auth", json={"username": "student", "password": "desingp"})
    assert r.status_code == 200
    token = r.get_json()["token"]
    assert client.get("/products", headers={"Authorization": token}).status_code == 200


def test_login_wrong_password(client):
    r = client.post("/auth", json={"username": "student", "password": "bad"})
    assert r.status_code == 401


@pytest.mark.parametrize("method,path", [
    ("get", "/products"), ("post", "/products"), ("get", "/categories"),
    ("post", "/categories"), ("delete", "/categories"), ("get", "/favorites"),
    ("post", "/favorites"), ("delete", "/favorites"),
])
def test_all_endpoints_require_token(client, method, path):
    assert getattr(client, method)(path).status_code == 401
    assert getattr(client, method)(path, headers={"Authorization": "x"}).status_code == 401


def test_products_list_get_filter(client, auth):
    assert len(client.get("/products", headers=auth).get_json()) > 0
    kids = client.get("/products?category=KIDS", headers=auth).get_json()
    assert kids and all(p["category"] == "kids" for p in kids)
    assert client.get("/products/1", headers=auth).get_json()["id"] == 1
    assert client.get("/products/9999", headers=auth).status_code == 404


def test_create_product_unique_ids(client, auth):
    body = {"name": "Hat", "category": "men", "price": 9}
    a = client.post("/products", json=body, headers=auth)
    b = client.post("/products", json=body, headers=auth)
    assert a.status_code == b.status_code == 201
    assert a.get_json()["product"]["id"] != b.get_json()["product"]["id"]


def test_create_product_validation(client, auth):
    assert client.post("/products", json={"name": "x"}, headers=auth).status_code == 400


def test_categories_crud(client, auth):
    assert client.post("/categories", json={"name": "pets"}, headers=auth).status_code == 201
    assert client.post("/categories", json={"name": "pets"}, headers=auth).status_code == 400
    names = [c["name"] for c in client.get("/categories", headers=auth).get_json()]
    assert "pets" in names
    assert client.delete("/categories", json={"name": "pets"}, headers=auth).status_code == 200
    assert client.delete("/categories", json={"name": "pets"}, headers=auth).status_code == 404
    names = [c["name"] for c in client.get("/categories", headers=auth).get_json()]
    assert "pets" not in names


def test_favorites_persist(client, auth):
    fav = {"user_id": 1, "product_id": 2}
    assert client.post("/favorites", json=fav, headers=auth).status_code == 201
    assert client.get("/favorites", headers=auth).get_json() == [fav]
    assert client.delete("/favorites", json=fav, headers=auth).status_code == 200
    assert client.get("/favorites", headers=auth).get_json() == []


def test_data_shared_across_requests(client, auth):
    client.post("/categories", json={"name": "a"}, headers=auth)
    client.post("/categories", json={"name": "b"}, headers=auth)
    ids = [c["id"] for c in client.get("/categories", headers=auth).get_json()]
    assert len(ids) == len(set(ids))
