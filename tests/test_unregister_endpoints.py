from urllib.parse import quote


ACTIVITY_NAME = "Chess Club"
ENCODED_ACTIVITY_NAME = quote(ACTIVITY_NAME, safe="")


def test_unregister_success_removes_participant(client):
    email = "michael@mergington.edu"

    unregister_response = client.delete(
        f"/activities/{ENCODED_ACTIVITY_NAME}/participants",
        params={"email": email},
    )

    assert unregister_response.status_code == 200
    assert unregister_response.json() == {
        "message": f"Unregistered {email} from {ACTIVITY_NAME}",
    }

    activities_response = client.get("/activities")
    participants = activities_response.json()[ACTIVITY_NAME]["participants"]
    assert email not in participants


def test_unregister_rejects_unknown_participant(client):
    unregister_response = client.delete(
        f"/activities/{ENCODED_ACTIVITY_NAME}/participants",
        params={"email": "not.registered@mergington.edu"},
    )

    assert unregister_response.status_code == 404
    assert unregister_response.json() == {
        "detail": "Participant not found for this activity",
    }


def test_unregister_rejects_unknown_activity(client):
    unregister_response = client.delete(
        "/activities/Unknown%20Club/participants",
        params={"email": "michael@mergington.edu"},
    )

    assert unregister_response.status_code == 404
    assert unregister_response.json() == {"detail": "Activity not found"}
