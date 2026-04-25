def test_get_activities_returns_activity_dictionary(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_get_activities_has_required_fields_for_each_activity(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    required_keys = {"description", "schedule", "max_participants", "participants"}

    for details in data.values():
        assert required_keys.issubset(details.keys())
        assert isinstance(details["participants"], list)
