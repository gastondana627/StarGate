# api/state.py
from http.server import BaseHTTPRequestHandler
import json
from game_logic import get_game_state

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        game_state = get_game_state()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(game_state).encode())