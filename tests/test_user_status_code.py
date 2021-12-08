def test_get_user_return_200(client):
    assert client.get("/api/user").status_code == 200, "Status code incorreto"


def test_post_user_return_201(client):
    assert client.post("/api/user").status_code == 201, "Status code incorreto"


def test_get_user_specific_return_200(client):
    assert client.get("/api/user/1").status_code == 200, "Status code incorreto"


def test_delete_user_specific_return_200(client):
    assert client.delete("/api/user/1").status_code == 200, "Status code incorreto"


def test_update_user_specific_return_200(client):
    assert client.patch("/api/user/1").status_code == 200, "Status code incorreto"


def test_get_user_specific_order_return_200(client):
    assert client.get("/api/user/1/order").status_code == 200, "Status code incorreto"


def test_get_user_specific_company_return_200(client):
    assert client.get("/api/user/1/company").status_code == 200, "Status code incorreto"
