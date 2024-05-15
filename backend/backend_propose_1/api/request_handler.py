import asyncio
from datetime import datetime, timedelta
from flask import jsonify, json
from assistant.chat import Chat


class RequestHandler():
    """
    The RequestHandler class manages incoming requests and orchestrates interactions with users.
    It utilizes the Chat class to handle conversations and responses.

    Attributes:
        active_users (dict): A dictionary containing active user objects, indexed by user ID.

    Methods:
        request_received(request: json) -> jsonify:
            Treats the incoming request and returns a JSON object response.
    """

    active_users = {}
    
    class User(Chat):
        def __init__(self, user_id, current_stage='welcome', orientation='', next_stage=''):
            """
            Initializes a User object with specified attributes.
            
            Parameters:
            - user_id (str): The unique identifier for the user.
            - current_stage (str): The current stage of interaction.
            - orientation (str): The orientation information of the user.
            - next_stage (str): The next stage of interaction.
            """
            self.user_id = user_id
            self.current_stage = current_stage
            self.orientation = orientation
            self.next_stage = next_stage
            self.last_interaction_time = datetime.now()  # Initialize last interaction time
            super().__init__(stage=current_stage)

    async def check_last_interaction(self):
        """
        Checks the last interaction time of all active users and removes inactive users.
        """
        now = datetime.now()
        inactive_users = []
        for user_id, user in self.active_users.items():
            if (now - user.last_interaction_time) > timedelta(minutes=10):
                inactive_users.append(user_id)
                print("Inactive user detected: ", user_id)
        
        for user_id in inactive_users:
            del self.active_users[user_id]
            print(f"User {user_id} removed due to inactivity.")

    async def request_received(self, request: json) -> jsonify:
        """
        Treats the incoming request and returns a JSON object response.
        [Currently missing]: Implementation for function that receives the information to close the conversation and deletes the user instance.\n
        Parameters:
            request (json): The incoming request JSON object.
        
        Returns:
            jsonify: A JSON object containing the response to the request.
        """
        try:
            request: dict = request.get_json()
            user_id: int = request.get("user_id")
            print("Request received by the API:", request)

            if user_id not in self.active_users:
                new_user = self.User(user_id=user_id)
                self.active_users[user_id] = new_user
                print("New user connected")
            
            user = self.active_users[user_id]
            user.set_user_attributes(request)
            user.last_interaction_time = datetime.now()  # Update last interaction time
            
            # Run the function to check last interaction in parallel
            asyncio.create_task(self.check_last_interaction())
            
            response = await user.main(request)

        except Exception as e:
            response = "I'm not feeling ok... Would you mind if we talk another time?"
            print(f"Error in request_received(): {e}")
            
        finally:
            return jsonify(response)
