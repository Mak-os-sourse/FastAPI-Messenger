class WebSocketError(ValueError):
    def __init__(self, error_name, *args):
        self.name = error_name
        super().__init__(*args)

class ActionError(WebSocketError):
    def __init__(self):
        super().__init__("Action not found", error_name="ActionError")