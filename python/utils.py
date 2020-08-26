"""Lab utility functions and classes."""

import json
from contextlib import contextmanager
from datetime import datetime
from typing import List
from uuid import uuid1

from crayons import blue, green, red, white
from devtools import debug
from pydantic import BaseModel, UUID1
from requests import HTTPError, Response


class AgentInfo(BaseModel):
    """Agent data model."""
    id: str
    codename: str


class MissionCheckpoint(BaseModel):
    """Mission Checkpoint data model."""
    number: int
    description: str
    data: dict = {}
    complete: bool = False


class MissionReport(BaseModel):
    """Mission Report data model."""
    id: UUID1
    mission: str
    timestamp: datetime
    agent: AgentInfo
    checkpoints: List[MissionCheckpoint] = []
    complete: bool = False


class MissionManager(object):
    """Lab Mission Manager."""

    def __init__(self, mission: str, agent_id: str, agent_codename: str):
        """Initialize a context manager for a new mission attempt."""
        self.report = MissionReport(
            id=uuid1(),
            mission=mission,
            timestamp=datetime.utcnow(),
            agent=AgentInfo(id=agent_id, codename=agent_codename),
        )

    @contextmanager
    def checkpoint(self, number: int, description: str):
        """Process a mission checkpoint."""
        print(
            f"{blue('==>', bold=True)} "
            f"{white(f'Begin Mission Checkpoint {number}', bold=True)}: "
            f"{description}"
        )

        checkpoint = MissionCheckpoint(
            number=number,
            description=description,
        )
        self.report.checkpoints.append(checkpoint)

        try:
            yield checkpoint

        # Here is where you can catch expected exception types and provide
        # useful outputs.
        except HTTPError as error:
            checkpoint.complete = False
            response: Response = error.response
            print(
                f"The API request failed; "
                f"Status Code: {response.status_code} {response.reason}"
            )
            try:
                body_data = response.json()
            except json.JSONDecodeError:
                pass
            else:
                print(f"Details:\n{json.dumps(body_data, indent=2)}")

        except Exception:
            checkpoint.complete = False
            raise

        else:
            checkpoint.complete = True

        if checkpoint.complete:
            print(
                f"{blue('==>', bold=True)} "
                f"{white(f'Mission Checkpoint {number}', bold=True)}: "
                f"{green('Complete!', bold=True)}"
            )
        else:
            print(
                f"{blue('==>', bold=True)} "
                f"{white(f'Mission Checkpoint {number}', bold=True)}: "
                f"{red('Incomplete.', bold=True)}"
            )

    def accomplished(self):
        """Mission Accomplished! Send the mission report."""
        # Ensure all checkpoints have been completed
        all_checkpoints_complete = all([
            checkpoint.complete for checkpoint in self.report.checkpoints
        ])
        if all_checkpoints_complete:
            self.report.complete = True

        if self.report.complete:
            print(
                f"{blue('==>', bold=True)} "
                f"{green(f'Mission Complete!', bold=True)}"
            )
        else:
            print(
                f"{blue('==>', bold=True)} "
                f"{red(f'Mission Failed.', bold=True)}"
            )
            return

        # This is where you would post your mission report to your API
        print("Sending Mission Report...")
        debug(self.report)
