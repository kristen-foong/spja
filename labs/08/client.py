import sys

"""
5 points.

Create a chat client with CMD parameters `server` and `port`.
1) Connect to the TCP server at <server>:<port>
2) Create a thread that will read lines from the input and send them to the server.
3) Read chat messages from the server and print them to stdout.
4) If the server disconnects, print "Server disconnected" and exit the program

Bonus task:
- implement a /setname <name> command, which will set your nickname in the chat.

Message format: each message is a JSON-encoded dictionary terminated with a newline ("\n").
The dictionary should have a key "type" and a key "data".

Client-server messages:
1) Send a message to chat - {"type": "message", "data": <content of chat message>}
2) Change your nickname - {"type": "set-name", "data": <nickname>}

Server-client messages:
1) New chat message - {"type": "message": "data": {"source": <nickname of sender>, "message": <content of chat message>}

Remember that TCP is a stream-oriented protocol, you must handle the separation of the stream
into messages terminated by newlines yourself. Your solution MUST work even if you use `socket.recv(1)`.

Example:
    $ python3 client.py 127.0.0.1 5555
    [Server]: 127.0.0.1:57354 has entered the chat
    hello
    127.0.0.1:57354: hello
    /setname Kobzol
    [Server]: 127.0.0.1:57354 renamed to Kobzol
    hello
    Kobzol: hello
"""

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 client.py <server> <port>")
        exit(1)
