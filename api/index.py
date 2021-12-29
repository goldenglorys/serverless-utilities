from http.server import BaseHTTPRequestHandler
import json
from ClassicUPS import UPSConnection


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_data = json.loads(self.rfile.read(content_len))
        tracking_id = post_data['tracking_id']
        ups = UPSConnection('ADAC6AB1040D9A52',
                    'Y789W4',
                    'tH^3@N75H@4vI',
                    debug=True)
        tracking = ups.tracking_info(tracking_id)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(
            json.dumps({"result": tracking}).encode()
        )
        return