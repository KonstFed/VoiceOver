from typing import Any
from addict import Dict

class State:
    def __init__(self, store: dict) -> None:
        self.store = Dict(store)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, str):
            return self.store["name"] == __value
        else:
            return self.store["name"] == __value.value

    def tojson(self):
        return self.store
    
    def __getattr__(self, __name: str) -> Any:
        return self.store.__getattr__(__name)


class WorkingState(State):
    def __init__(self) -> None:
        super().__init__({"name": "working"})


class RedactState(State):
    def __init__(self, name_value: str, message_id) -> None:
        super().__init__({"name": name_value, "msg_id": message_id})


class User:
    def __init__(
        self, telegram_id: int, username: str, state: State, voice: int = 0
    ) -> None:
        self.telegram_id = telegram_id
        self.username = username
        self.state = state
        self.voice = voice

    def update(self, user):
        self.telegram_id = user.telegram_id
        self.username = user.username
        self.state = user.state
        self.voice = user.voice

    def tojson(self):
        return {
            "telegram_id": self.telegram_id,
            "username": self.username,
            "voice": self.voice,
            "state": self.state.tojson(),
        }
