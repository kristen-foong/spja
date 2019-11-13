import json
import socket
import sys
import threading


def send(socket, str):
    return socket.sendall("{}\n".format(str).encode())


def handle_message(msg):
    if msg["type"] == "message":
        payload = msg["data"]
        source = payload["source"]
        content = payload["message"]
        print("{}: {}".format(source, content))
    else:
        print("Unknown message type {} from server".format(msg["type"]))


def chat_process(client):
    while True:
        line = input()
        if line.startswith("/setname"):
            cmd = line.split()
            if len(cmd) < 2:
                print("Usage: /setname <name>")
            else:
                name = cmd[1]
                send(client, json.dumps({
                    "type": "set-name",
                    "data": name
                }))
        elif line.startswith("/history"):
            send(client, json.dumps({
                "type": "history",
            }))
        elif line.startswith("/users"):
            send(client, json.dumps({
                "type": "users",
            }))
        else:
            send(client, json.dumps({
                "type": "message",
                "data": line
            }))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python client.py <server> <port>")
        exit(1)

    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))

    thread = threading.Thread(target=chat_process, args=(client, ))
    thread.daemon = True
    thread.start()

    buffer = ""
    try:
        while True:
            data = client.recv(1)
            if not data:
                print("Server disconnected")
                break
            buffer += data.decode()
            while "\n" in buffer:
                index = buffer.index('\n')
                line = buffer[:index]
                handle_message(json.loads(line))
                buffer = buffer[index + 1:]
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

    client.close()
