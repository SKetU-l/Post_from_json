import http.server
import os
import socketserver

port = os.environ.get("APP_PORT")

if port:

    class Server(socketserver.TCPServer):
        def __init__(self, server_address, HandlerClass):
            super().__init__(server_address, HandlerClass, bind_and_activate=False)
            self.allow_reuse_address = True
            self.allow_reuse_port = True
            self.server_bind()
            self.server_activate()

    class MyHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Miku_got_radish")

        def log_message(self, *args, **kwargs):
            pass

    address = ("", int(port))
    httpd = Server(address, MyHandler)

    try:
        print(f"Server Started on Port: {port}.")
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        httpd.shutdown()
        print("\nServer Stopped.")
