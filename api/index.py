from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        message = {
                    "DATABASE": os.getenv("DATABASE_URL"),
                    "CREDS_JSON_STR": os.getenv("CREDS_JSON_STR")
                }
        self.wfile.write(message.encode())
        return