def test_get_company_return_200(client):
    assert client.get("/api/company").status_code == 200, "Status code incorreto"


def test_post_company_return_201(client):
    assert client.post("/api/company").status_code == 201, "Status code incorreto"


def test_get_company_specific_return_200(client):
    assert client.get("/api/company/1").status_code == 200, "Status code incorreto"


def test_delete_company_specific_return_200(client):
    assert client.post("/api/company/1").status_code == 200, "Status code incorreto"


def test_update_company_specific_return_200(client):
    assert client.post("/api/company/1").status_code == 200, "Status code incorreto"


def test_get_company_specific_user_return_200(client):
    assert client.get("/api/company/1/user").status_code == 200, "Status code incorreto"