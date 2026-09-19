from fastapi.testclient import TestClient


def test_create_project(client: TestClient, auth_headers: dict[str, str]) -> None:
    response = client.post(
        "/api/v1/projects",
        json={"name": "Test Project", "description": "A test", "project_type": "carbon"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Test Project"
    assert body["project_type"] == "carbon"


def test_create_project_requires_auth(client: TestClient) -> None:
    response = client.post("/api/v1/projects", json={"name": "No Auth"})
    assert response.status_code == 401


def test_list_projects_only_returns_own(client: TestClient, auth_headers: dict[str, str]) -> None:
    client.post("/api/v1/projects", json={"name": "Mine"}, headers=auth_headers)
    response = client.get("/api/v1/projects", headers=auth_headers)
    assert response.status_code == 200
    names = [p["name"] for p in response.json()]
    assert "Mine" in names


def test_get_project_not_found(client: TestClient, auth_headers: dict[str, str]) -> None:
    response = client.get("/api/v1/projects/99999", headers=auth_headers)
    assert response.status_code == 404
