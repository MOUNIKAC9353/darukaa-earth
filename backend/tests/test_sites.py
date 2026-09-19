from fastapi.testclient import TestClient

SAMPLE_POLYGON = {
    "type": "Polygon",
    "coordinates": [
        [
            [74.240, 21.370],
            [74.250, 21.370],
            [74.250, 21.380],
            [74.240, 21.380],
            [74.240, 21.370],
        ]
    ],
}


def _create_project(client: TestClient, auth_headers: dict[str, str]) -> int:
    response = client.post("/api/v1/projects", json={"name": "Site Project"}, headers=auth_headers)
    return response.json()["id"]


def test_create_site(client: TestClient, auth_headers: dict[str, str]) -> None:
    project_id = _create_project(client, auth_headers)
    response = client.post(
        f"/api/v1/projects/{project_id}/sites",
        json={"name": "Plot A", "geometry": SAMPLE_POLYGON},
        headers=auth_headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Plot A"
    assert body["geometry"]["type"] == "Polygon"
    assert body["area_hectares"] > 0


def test_add_and_list_site_metrics(client: TestClient, auth_headers: dict[str, str]) -> None:
    project_id = _create_project(client, auth_headers)
    site_resp = client.post(
        f"/api/v1/projects/{project_id}/sites",
        json={"name": "Plot B", "geometry": SAMPLE_POLYGON},
        headers=auth_headers,
    )
    site_id = site_resp.json()["id"]

    metric_resp = client.post(
        f"/api/v1/sites/{site_id}/metrics",
        json={
            "recorded_date": "2026-01-01",
            "carbon_tons": 12.5,
            "biodiversity_index": 55.0,
            "ndvi": 0.42,
        },
        headers=auth_headers,
    )
    assert metric_resp.status_code == 201

    list_resp = client.get(f"/api/v1/sites/{site_id}/metrics", headers=auth_headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1


def test_site_not_found_for_other_user(client: TestClient, auth_headers: dict[str, str]) -> None:
    response = client.get("/api/v1/sites/99999", headers=auth_headers)
    assert response.status_code == 404


def test_list_all_sites_spans_projects_and_is_owner_scoped(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    project_a = _create_project(client, auth_headers)
    project_b = client.post(
        "/api/v1/projects", json={"name": "Second Project"}, headers=auth_headers
    ).json()["id"]
    client.post(
        f"/api/v1/projects/{project_a}/sites",
        json={"name": "Plot A", "geometry": SAMPLE_POLYGON},
        headers=auth_headers,
    )
    client.post(
        f"/api/v1/projects/{project_b}/sites",
        json={"name": "Plot C", "geometry": SAMPLE_POLYGON},
        headers=auth_headers,
    )

    client.post(
        "/api/v1/auth/register",
        json={"email": "other@example.com", "full_name": "Other User", "password": "password123"},
    )
    other_login = client.post(
        "/api/v1/auth/login", json={"email": "other@example.com", "password": "password123"}
    )
    other_headers = {"Authorization": f"Bearer {other_login.json()['access_token']}"}

    response = client.get("/api/v1/sites", headers=auth_headers)
    assert response.status_code == 200
    names = {site["name"] for site in response.json()}
    assert names == {"Plot A", "Plot C"}
    assert all("project_name" in site for site in response.json())

    other_response = client.get("/api/v1/sites", headers=other_headers)
    assert other_response.status_code == 200
    assert other_response.json() == []
