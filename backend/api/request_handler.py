import asyncio
from datetime import datetime, timedelta
from flask import jsonify, json


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
           
            response = await user.main(request)

        except Exception as e:
            response = "I'm not feeling ok... Would you mind if we talk another time?"
            print(f"Error in request_received(): {e}")
            
        finally:
            return jsonify(response)
