def test_project_crud_and_unique_name(client):
    r = client.post("/projects/", json={"name": "Gamma", "description": "Project Gamma"})
    assert r.status_code == 201, r.text
    project = r.json()

    r = client.post("/projects/", json={"name": "Gamma", "description": "Duplicate"})
    assert r.status_code == 409

    r = client.get(f"/projects/{project['id']}")
    assert r.status_code == 200

    r = client.patch(f"/projects/{project['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    assert r.json()["description"] == "Updated"

    r = client.get("/projects/", params={"sort": "id", "skip": 0, "limit": 10})
    assert r.status_code == 200
    rows = r.json()
    assert any(row["id"] == project["id"] for row in rows)

    r = client.get("/projects/", params={"sort": "invalid_field"})
    assert r.status_code == 422

    r = client.delete(f"/projects/{project['id']}")
    assert r.status_code == 204

    r = client.get(f"/projects/{project['id']}")
    assert r.status_code == 404
