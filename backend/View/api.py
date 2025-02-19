from flask import Flask, request
from flask_cors import CORS
from .RequestHandler import RequestHandler


rh = RequestHandler()
app = Flask(__name__)
CORS(app)


@app.route('/kobu-assistant', methods=['POST'])
async def receiveMessage():
    return await rh.request_handler(request)
