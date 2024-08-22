import http.server
import socketserver

class RedirectHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Define the path to redirect to
        redirect_path = '/new-path'
        
        # If the request path is '/', redirect to the new path
        if self.path == '/':
            self.send_response(302)
            self.send_header('Location', redirect_path)
            self.end_headers()
        else:
            # Handle the request normally for other paths
            super().do_GET()

# Define the server address and port
server_address = ('', 8000)

# Create an instance of the custom handler
handler = RedirectHandler

# Create the HTTP server
httpd = socketserver.TCPServer(server_address, handler)

print("Serving at port", server_address[1])
# Start the server
httpd.serve_forever()
