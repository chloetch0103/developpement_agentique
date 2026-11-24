from typing import TypedDict


class State(TypedDict):
    task: str
    spec: str
    code: str
    attempts: int
