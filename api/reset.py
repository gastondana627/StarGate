# api/reset.py
from http.server import BaseHTTPRequestHandler
import json
from game_logic import reset_game

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        reset_game()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success"}).encode())
