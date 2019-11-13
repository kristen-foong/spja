import json
import sys
import traceback

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

MAX_NUMBER_OF_USERS = 1


class Chat:
    def __init__(self):
        self.users = {}
        self.messages = []

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
        self.messages.append(msg)
        print("{}: {}".format(user.name, msg))
        self._broadcast(user, msg)

    def _broadcast(self, source, msg):
        try:
            for receiver in self.users.values():
                receiver.on_message(source, msg)
        except:
            traceback.print_exc()


class ChatProtocol(LineReceiver):
    def __init__(self, chat, addr):
        super().__init__()
        self.chat = chat
        self.addr = addr
        self.name = "{}:{}".format(addr.host, addr.port)
        self.delimiter = b"\n"

    def on_message(self, source, msg):
        self.sendLine(json.dumps({
            "type": "message",
            "data": {
                "source": source.name,
                "message": msg
            }
        }).encode())

    def lineReceived(self, line):
        try:
            message = json.loads(line.strip())
            if message["type"] == "message":
                self.chat.post_message(self, message["data"])
            elif message["type"] == "set-name":
                self.chat.user_rename(self.name, message["data"])
                self.name = message["data"]
            else:
                print("Unknown message type {} from {}".format(message["type"], self.name))
        except Exception as e:
            print("Client {} error: {}".format(self.addr, e))

    def connectionMade(self):
        super().connectionMade()
        self.chat.user_connect(self)

    def connectionLost(self, reason=None):
        super().connectionLost(reason)
        self.chat.user_disconnect(self)


class ChatFactory(Factory):
    def __init__(self, chat):
        self.chat = chat

    def buildProtocol(self, addr):
        if self.chat.has_free_slots():
            return ChatProtocol(self.chat, addr)
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python server.py <port>")
        exit(1)

    PORT = int(sys.argv[1])

    print("Server listening on 127.0.0.1:{}".format(PORT))

    chat = Chat()
    endpoint = TCP4ServerEndpoint(reactor, PORT)
    endpoint.listen(ChatFactory(chat))
    reactor.run()
