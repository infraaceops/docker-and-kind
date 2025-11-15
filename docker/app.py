from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello from Python app in scratch!")

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 80), Handler)
    print("Server running on port 80")
    server.serve_forever()
