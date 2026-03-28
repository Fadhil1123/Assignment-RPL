def test_create_get_patch_and_delete_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    note_id = data["id"]
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200

    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404


def test_note_validation_and_project_assignment(client):
    r = client.post("/notes/", json={"title": "   ", "content": "body"})
    assert r.status_code == 422

    r = client.post("/notes/", json={"title": "Good", "content": "   "})
    assert r.status_code == 422

    r = client.post("/projects/", json={"name": "Beta", "description": "Project Beta"})
    assert r.status_code == 201
    project_id = r.json()["id"]

    r = client.post(
        "/notes/",
        json={"title": "Project Note", "content": "Attached to project", "project_id": project_id},
    )
    assert r.status_code == 201, r.text
    note_id = r.json()["id"]

    r = client.patch(f"/notes/{note_id}", json={"project_id": 999999})
    assert r.status_code == 404


def test_note_pagination_sort_filter_and_invalid_sort(client):
    for index in range(8):
        r = client.post(
            "/notes/",
            json={"title": f"Title {index}", "content": f"Body {index}"},
        )
        assert r.status_code == 201, r.text

    r = client.get("/notes/", params={"sort": "id", "skip": 2, "limit": 3})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 3
    assert rows[0]["id"] < rows[1]["id"]

    r = client.get("/notes/", params={"sort": "-id", "limit": 2})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 2
    assert rows[0]["id"] > rows[1]["id"]

    r = client.get("/notes/", params={"q": "Body 3", "sort": "id"})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) >= 1
    assert any("Body 3" in row["content"] for row in rows)

    r = client.get("/notes/", params={"sort": "invalid"})
    assert r.status_code == 422
