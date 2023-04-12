import socketserver
from flag import FLAG


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        if data == b"PING":
            msg = FLAG
        else:
            msg = b"I didnt get a `PING`..."
        socket.sendto(msg, self.client_address)


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 21000
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
