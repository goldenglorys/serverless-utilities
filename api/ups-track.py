from ClassicUPS import UPSConnection


ups = UPSConnection('ADAC6AB1040D9A52',
                    'Y789W4',
                    'tH^3@N75H@4vI',
                    debug=True)

tracking = ups.tracking_info('1Z12345E0291980793')
print(tracking.delivered)
print(tracking.in_transit)
print(tracking.shipment_activities)
print(tracking)
# from http.server import BaseHTTPRequestHandler
# from urllib import parse
# class handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         s = self.path
#         dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
#         self.send_response(200)
#         self.send_header('Content-type','text/plain')
#         self.end_headers()
#         if "name" in dic:
#             message = "Hello, " + dic["name"] + "!"
#         else:
#             message = "Hello, stranger!"
#         self.wfile.write(message.encode())
#         return