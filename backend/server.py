import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import dotenv_values
from src.routes import Router

config = dotenv_values(".env")
server_address = (
    config.get("SERVER_HOSTNAME") or "localhost",
    int(config.get("SERVER_PORT") or "8000")
)

class RequestHandler(BaseHTTPRequestHandler):
    def parse_json_data(self):
        try:
            content_len = int(self.headers['Content-Length'])
            return json.loads(self.rfile.read(content_len))
        except Exception:
            raise

    def finish_request(self, status, response):
        self.send_response(status)
        if not response == None:
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_header("Content-Type", "text/plain")
            self.end_headers()

    def do_GET(self):
        [status, response] = Router.handle_get(self.path)
        self.finish_request(status, response)

    def do_POST(self):
        try:
            data = self.parse_json_data()
            [status, response] = Router.handle_post(self.path, data=data)
            self.finish_request(status, response)
        except json.JSONDecodeError:
            self.finish_request(400, {
                'status': 'error',
                'message': 'Invalid JSON data'
            })

    def do_PATCH(self):
        try:
            data = self.parse_json_data()
            [status, response] = Router.handle_patch(self.path, data=data)
            self.finish_request(status, response)
        except json.JSONDecodeError:
            self.finish_request(400, {
                'status': 'error',
                'message': 'Invalid JSON data'
            })

    def do_DELETE(self):
        [status, response] = Router.handle_delete(self.path)
        self.finish_request(status, response)

if __name__ == "__main__":
    with HTTPServer(server_address, RequestHandler) as server:
        print("Sever running in port", server_address[1])
        server.serve_forever()
