from urllib.parse import quote


ACTIVITY_NAME = "Chess Club"
ENCODED_ACTIVITY_NAME = quote(ACTIVITY_NAME, safe="")


def test_signup_success_adds_participant(client):
    email = "new.student@mergington.edu"

    signup_response = client.post(
        f"/activities/{ENCODED_ACTIVITY_NAME}/signup",
        params={"email": email},
    )

    assert signup_response.status_code == 200
    assert signup_response.json() == {
        "message": f"Signed up {email} for {ACTIVITY_NAME}",
    }

    activities_response = client.get("/activities")
    participants = activities_response.json()[ACTIVITY_NAME]["participants"]
    assert email in participants


def test_signup_rejects_duplicate_participant(client):
    signup_response = client.post(
        f"/activities/{ENCODED_ACTIVITY_NAME}/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert signup_response.status_code == 400
    assert signup_response.json() == {
        "detail": "Student already signed up for this activity",
    }


def test_signup_rejects_unknown_activity(client):
    signup_response = client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": "new.student@mergington.edu"},
    )

    assert signup_response.status_code == 404
    assert signup_response.json() == {"detail": "Activity not found"}
