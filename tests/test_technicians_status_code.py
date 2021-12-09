def test_get_technicians_return_200(client):
    assert client.get("/api/technicians").status_code == 200, "Status code incorreto"


def test_post_technicians_return_201(client):
    assert client.post("/api/technicians").status_code == 201, "Status code incorreto"


def test_get_technicians_specific_return_200(client):
    assert client.get("/api/technicians/1").status_code == 200, "Status code incorreto"


def test_delete_technicians_specific_return_200(client):
    assert client.delete("/api/technicians/1").status_code == 200, "Status code incorreto"


def test_update_technicians_specific_return_200(client):
    assert client.patch("/api/technicians/1").status_code == 200, "Status code incorreto"


def test_get_technicians_specific_order_return_200(client):
    assert client.get("/api/technicians/1/order").status_code == 200, "Status code incorreto"