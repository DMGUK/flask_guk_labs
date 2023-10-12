#server
from http.server import HTTPServer, CGIHTTPRequestHandler
server_address = ("127.0.0.1", 9999)

print("The server is working. Awayting input.....")

httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()

