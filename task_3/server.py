import socket
import threading
import sys

clients = []
subscribers = {}

def handle_client(client_socket, client_address, role, topic):
    global clients
    global subscribers

    print(f"Client {client_address} connected as {role} on topic {topic}")

    if role == "SUBSCRIBER":
        if topic not in subscribers:
            subscribers[topic] = []
        subscribers[topic].append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message or message.lower() == "terminate":
                print(f"Client {client_address} disconnected")
                if role == "SUBSCRIBER":
                    subscribers[topic].remove(client_socket)
                clients.remove(client_socket)
                client_socket.close()
                break

            if role == "PUBLISHER":
                print(f"Message from Publisher {client_address} on topic {topic}: {message}")
                if topic in subscribers:
                    for subscriber in subscribers[topic]:
                        try:
                            subscriber.send(f"Message from Publisher {client_address} on topic {topic}: {message}".encode())
                        except:
                            subscribers[topic].remove(subscriber)
        except:
            if role == "SUBSCRIBER":
                subscribers[topic].remove(client_socket)
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)

    print(f"Server started and listening on port {port}")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        role_topic = client_socket.recv(1024).decode().split()
        if len(role_topic) != 2:
            client_socket.close()
            continue
        role, topic = role_topic
        client_handler = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address, role, topic)
        )
        client_handler.start()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
