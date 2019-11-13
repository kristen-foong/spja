import collections
import json
import socket
import sys
import threading
import traceback

MAX_NUMBER_OF_USERS = 100


def send(socket, str):
    return socket.sendall("{}\n".format(str).encode())


class User:
    def __init__(self, chat, addr, socket):
        self.chat = chat
        self.addr = addr
        self.socket = socket
        self.name = "{}:{}".format(*addr)

    def execute(self):
        try:
            for message in iter_messages(self.socket):
                if message["type"] == "message":
                    self.chat.post_message(self, message["data"])
                elif message["type"] == "history":
                    self.on_message(self.chat, repr(tuple(self.chat.messages)))
                elif message["type"] == "users":
                    self.on_message(self.chat, repr(tuple(user.name for user in self.chat.users.values())))
                elif message["type"] == "set-name":
                    self.chat.user_rename(self.name, message["data"])
                    self.name = message["data"]
                else:
                    print("Unknown message type {} from {}".format(message["type"], self.name))

        except Exception as e:
            print("Client {} error: {}".format(self.addr, e))
        finally:
            self.chat.user_disconnect(self)
        self.socket.close()

    def on_message(self, source, msg):
        send(self.socket, json.dumps({
            "type": "message",
            "data": {
                "source": source.name,
                "message": msg
            }
        }))


class Chat:
    def __init__(self):
        self.users = {}

        # use a fixed size queue to avoid running out of memory
        self.messages = collections.deque(maxlen=1000)

    @property
    def name(self):
        return "[Server]"

    def has_free_slots(self):
        return len(self.users) < MAX_NUMBER_OF_USERS

    def user_connect(self, user):
        self.users[user.addr] = user
        print("Client connected: {}".format(user.name))
        self._broadcast(self, "{} has entered the chat".format(user.name))

    def user_disconnect(self, user):
        del self.users[user.addr]
        print("Client disconnected: {}".format(user.name))
        self._broadcast(self, "{} has left the chat".format(user.name))

    def user_rename(self, oldname, name):
        msg = "{} renamed to {}".format(oldname, name)
        print(msg)
        self._broadcast(self, msg)

    def post_message(self, user, msg):
        assert user.addr in self.users
        self.messages.append((user.name, msg))
        print("{}: {}".format(user.name, msg))
        self._broadcast(user, msg)

    def _broadcast(self, source, msg):
        try:
            users = list(self.users.values())
            for receiver in users:
                receiver.on_message(source, msg)
        except:
            traceback.print_exc()


def init_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', port))
    sock.listen(10)
    return sock


def iter_messages(socket):
    buffer = ""
    while True:
        data = socket.recv(1)
        if not data:
            break
        buffer += data.decode()
        while '\n' in buffer:
            index = buffer.index('\n')
            line = buffer[:index]
            yield json.loads(line)
            buffer = buffer[index + 1:]


def chat_server(chat, port):
    sock = init_server(port)

    try:
        while True:
            client, addr = sock.accept()
            if chat.has_free_slots():
                user = User(chat, addr, client)
                chat.user_connect(user)
                thread = threading.Thread(target=user.execute)
                thread.daemon = True
                thread.start()
            else:
                client.close()
    except KeyboardInterrupt:
        print("Server exiting")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python server.py <port>")
        exit(1)

    PORT = int(sys.argv[1])

    print("Server listening on 127.0.0.1:{}".format(PORT))

    chat = Chat()
    chat_server(chat, PORT)
