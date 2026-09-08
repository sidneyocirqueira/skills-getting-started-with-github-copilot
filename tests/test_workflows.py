from urllib.parse import quote


def test_signup_then_unregister_restores_activity_state(client):
    # Arrange
    activity = "Soccer Club"
    email = "workflow+student@mergington.edu"
    initial_activity = client.get("/activities").json()[activity]
    initial_participant_count = len(initial_activity["participants"])
    initial_spots = initial_activity["max_participants"] - initial_participant_count

    # Act
    signup_response = client.post(
        f"/activities/{quote(activity)}/signup",
        params={"email": email},
    )

    # Assert
    assert signup_response.status_code == 200
    signed_up_activity = client.get("/activities").json()[activity]
    assert email in signed_up_activity["participants"]
    assert len(signed_up_activity["participants"]) == initial_participant_count + 1

    # Act
    unregister_response = client.delete(
        f"/activities/{quote(activity)}/participants/{quote(email, safe='')}"
    )

    # Assert
    assert unregister_response.status_code == 200
    final_activity = client.get("/activities").json()[activity]
    assert email not in final_activity["participants"]
    assert len(final_activity["participants"]) == initial_participant_count
    assert final_activity["max_participants"] - len(final_activity["participants"]) == initial_spots
