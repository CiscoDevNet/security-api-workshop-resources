#!/usr/bin/env python
"""Example mission usage."""

import os
import random
import string

import requests
import webexteamssdk

from utils import MissionManager


YOUR_CODENAME = "Cipher"
REMOTE_CONTACT = "oxsannikova@gmail.com"
#WEBEX_TEAMS_ACCESS_TOKEN = os.environ.get("WEBEX_TEAMS_ACCESS_TOKEN")
WEBEX_TEAMS_ACCESS_TOKEN = "Y2ZhYzc3MDMtMDQ4OC00M2U0LThiZjYtZTQxNmYzYmM0NTZhY2I4NWNlN2QtMWRl_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"

teams = webexteamssdk.WebexTeamsAPI(WEBEX_TEAMS_ACCESS_TOKEN)
me = teams.people.me()
mission = MissionManager(
    mission="Sample Mission",
    agent_id=me.id,
    agent_codename=YOUR_CODENAME,
)
passcode = "".join([random.choice(string.digits) for i in range(6)])


# You can use the checkpoints as function decorators,
# if you don't want to capture checkpoint data
@mission.checkpoint(1, "Create a Room")
def create_room() -> webexteamssdk.Room:
    """Use the webexteamssdk to create a room."""
    return teams.rooms.create(title="Sample Mission")


def add_contact_to_room(room_id: str, contact: str):
    """Use the webexteamssdk to add the contact to the room."""
    # You can also use it as a context handler to catch errors and capture
    # checkpoint data.
    with mission.checkpoint(2, "Add the Contact to the Room") as checkpoint:
        membership = teams.memberships.create(room_id, personEmail=contact)
        checkpoint.data["contact_id"] = membership.personId
        checkpoint.data["contact_name"] = membership.personDisplayName


def post_message(room_id: str, message: str):
    """Use the raw Webex Teams APIs to post a message to the room."""
    url = "https://MISSION"
    headers = {
        "Authorization": f"Bearer {WEBEX_TEAMS_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    body = {"roomId": room_id, "markdown": message}
    with mission.checkpoint(3, "Post a Message") as checkpoint:
        print(f"Sending a request to URL: {url}")

        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()

        message_data = response.json()
        checkpoint.data["message_id"] = message_data.get("messageId")


def main():
    """Run the mission."""
    room = create_room()
    add_contact_to_room(room_id=room.id, contact=REMOTE_CONTACT)
    post_message(room_id=room.id, message=f"The passcode is {passcode}.")
    mission.accomplished()


if __name__ == "__main__":
    main()
