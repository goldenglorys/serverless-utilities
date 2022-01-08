from http.server import BaseHTTPRequestHandler
from urllib import parse
import os
import json
from ClassicUPS import UPSConnection


LICENSE_NUMBER = os.getenv("LICENSE_NUMBER")
USER_ID = os.getenv("USER_ID")
PASSWORD = os.getenv("PASSWORD")


class TrackAPI():
    def track_by_id(self, tracking_id):
        ups = UPSConnection(
            LICENSE_NUMBER,
            USER_ID,
            PASSWORD,
            debug=True
        )
        tracking_result = ups.tracking_info(tracking_id)
        return tracking_result


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_data = json.loads(self.rfile.read(content_len))
        d = TrackAPI()
        tracking_result = d.track_by_id(
            post_data['tracking_id']
        )
        result_data = {
            "delivered": str(tracking_result.delivered),
            "in_transit": str(tracking_result.in_transit),
            "shipment_activities": str(tracking_result.shipment_activities)
        }
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin",
                         "https://flow.inv.tech/")
        self.end_headers()
        self.wfile.write(
            json.dumps(result_data).encode()
        )