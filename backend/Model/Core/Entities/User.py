class User:
    def __init__(self, user_id: int, request: dict):
        self.user_id: int = user_id
        self.request: dict = request
        self.user_input: str = self.request.user_input
        self.lead = None
