import socket
import threading

BUFFER_SIZE = 1024

publisher_sockets = []
subscriber_sockets = []
lock = threading.Lock()


def handle_client(client_socket, client_role):
    global subscriber_sockets
    global publisher_sockets

    is_publisher = client_role == "PUBLISHER"

    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            if message == "terminate":
                print("Terminate command received. Disconnecting client.")
                break

            if is_publisher:
                with lock:
                    for subscriber_socket in subscriber_sockets:
                        subscriber_socket.send(message.encode("utf-8"))
            print(
                f"Message from {'Publisher' if is_publisher else 'Subscriber'}: {message}"
            )
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()
    with lock:
        if is_publisher:
            publisher_sockets.remove(client_socket)
        else:
            subscriber_sockets.remove(client_socket)
    print("Client disconnected")


def main(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    print(f"Server is listening on port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")

        role = client_socket.recv(BUFFER_SIZE).decode("utf-8")
        is_publisher = role == "PUBLISHER"

        with lock:
            if is_publisher:
                publisher_sockets.append(client_socket)
            else:
                subscriber_sockets.append(client_socket)

        client_handler = threading.Thread(
            target=handle_client, args=(client_socket, role)
        )
        client_handler.start()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])
    main(port)
