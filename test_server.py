from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello, it works!')

print('Starting server on port 5000...')
httpd = HTTPServer(('', 5000), Handler)
print('Server is running at http://localhost:5000')
httpd.serve_forever() 