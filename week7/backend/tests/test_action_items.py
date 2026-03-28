def test_create_complete_get_patch_and_delete_action_item(client):
    r = client.post("/action-items/", json={"description": "Ship it"})
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    assert r.json()["completed"] is True

    r = client.get(f"/action-items/{item['id']}")
    assert r.status_code == 200

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    assert r.json()["description"] == "Updated"

    r = client.delete(f"/action-items/{item['id']}")
    assert r.status_code == 204

    r = client.get(f"/action-items/{item['id']}")
    assert r.status_code == 404


def test_action_item_validation_and_project_link(client):
    r = client.post("/action-items/", json={"description": "   "})
    assert r.status_code == 422

    r = client.post("/projects/", json={"name": "Alpha", "description": "Project Alpha"})
    assert r.status_code == 201, r.text
    project_id = r.json()["id"]

    r = client.post(
        "/action-items/", json={"description": "Task with project", "project_id": project_id}
    )
    assert r.status_code == 201, r.text
    item_id = r.json()["id"]

    r = client.patch(f"/action-items/{item_id}", json={"project_id": 999999})
    assert r.status_code == 404


def test_action_item_pagination_sort_and_invalid_sort(client):
    for index in range(6):
        r = client.post(
            "/action-items/",
            json={"description": f"Task {index}", "project_id": None},
        )
        assert r.status_code == 201, r.text

    r = client.get("/action-items/", params={"sort": "id", "skip": 1, "limit": 2})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 2
    assert rows[0]["id"] < rows[1]["id"]

    r = client.get("/action-items/", params={"sort": "-id", "limit": 3})
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 3
    assert rows[0]["id"] > rows[1]["id"]

    r = client.get("/action-items/", params={"sort": "unknown_field"})
    assert r.status_code == 422
