def test_get_order_return_200(client):
    assert client.get("/api/order").status_code == 200, "Status code incorreto"


def test_post_order_return_201(client):
    assert client.post("/api/order").status_code == 201, "Status code incorreto"


def test_get_order_specific_return_200(client):
    assert client.get("/api/order/1").status_code == 200, "Status code incorreto"


def test_delete_order_specific_return_200(client):
    assert client.delete("/api/order/1").status_code == 200, "Status code incorreto"


def test_update_order_specific_return_200(client):
    assert client.patch("/api/order/1").status_code == 200, "Status code incorreto"


def test_get_order_specific_user_return_200(client):
    assert client.get("/api/order/1/user").status_code == 200, "Status code incorreto"


def test_get_order_specific_technicians_return_200(client):
    assert client.get("/api/order/1/technicians").status_code == 200, "Status code incorreto"
