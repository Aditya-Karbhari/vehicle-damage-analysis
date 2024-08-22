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
        elif self.path == redirect_path:
            # Serve custom content for the new path
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            content = """
            <html>
            <head>
                <title>Redirected Page</title>
            </head>
            <body>
                <h1>Welcome to the new path!</h1>
                <p>This is the content of the new path.</p>
            </body>
            </html>
            """
            self.wfile.write(content.encode('utf-8'))
        else:
            # Handle the request normally for other paths
            super().do_GET()

# Define the server address and port
server_address = ('', 8001)

# Create an instance of the custom handler
handler = RedirectHandler

# Create the HTTP server
httpd = socketserver.TCPServer(server_address, handler)

print("Serving at port", server_address[1])
# Start the server
httpd.serve_forever()
