from typing import Any


class WebSocketError(ValueError):
    def __init__(self, error_name: str, *args: Any) -> None:
        self.name = error_name
        super().__init__(*args)


class ActionError(WebSocketError):
    def __init__(self) -> None:
        super().__init__("ActionError", "Action not found")
