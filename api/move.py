# api/move.py
from http.server import BaseHTTPRequestHandler
from urllib import parse
import json
from game_logic import move_robot, get_game_state

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
        dx = int(dic.get("dx", 0))
        dy = int(dic.get("dy", 0))
        move_robot(dx, dy)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(get_game_state()).encode())