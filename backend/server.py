from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from dotenv import dotenv_values
from src.models.event import Event

config = dotenv_values(".env")
server_address = (
    config.get("SERVER_HOSTNAME") or "localhost",
    int(config.get("SERVER_PORT") or "8000")
)

if __name__ == "__main__":
    print("TODO")
