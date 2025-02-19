class User:
    def __init__(self, user_id=int, request=dict):
        self.user_id = user_id
        self.request = request
        self.user_input = self.request.get('user_input')
        self.lead = None
