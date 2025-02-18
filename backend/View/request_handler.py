import asyncio
from flask import jsonify, json
from backend.Interface.assistant_interface import interface_controller


class RequestHandler():
    async def _verify_request(self, request: json) -> jsonify:
        return request
    
    async def request_handler(self, request: json) -> jsonify:
        try:
            verified_request = self._verify_request(request)
            response = interface_controller(verified_request)
                
        except Exception as e:
            response = "I'm not feeling ok... Would you mind if we talk another time?"
            print(f"Error in request_received(): {e}")
            
        finally:
            print("RequestHandler - Response to be send:\n", response)
            return jsonify(response)
