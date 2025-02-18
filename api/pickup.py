# api/pickup.py
from http.server import BaseHTTPRequestHandler
import json
from game_logic import pick_up_rock, get_game_state

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        result = pick_up_rock()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"result": result, "gameState": get_game_state()}).encode())