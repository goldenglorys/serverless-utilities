from http.server import BaseHTTPRequestHandler
from urllib import parse
import json


class handler(BaseHTTPRequestHandler):
    # def do_GET(self):
    #     s = self.path
    #     dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
    #     self.send_response(200)
    #     self.send_header('Content-type','text/plain')
    #     self.end_headers()
    #     if "name" in dic:
    #         message = "Hello, " + dic["name"] + "!"
    #     else:
    #         message = "Hello, stranger!"
    #     self.wfile.write(message.encode())
    #     return

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_data = json.loads(self.rfile.read(content_len))
        tracking_id = post_data['tracking_id']
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(
            json.dumps({"url": tracking_id}).encode()
        )
        return