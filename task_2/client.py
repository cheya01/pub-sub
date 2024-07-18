import socket
import threading
import sys

BUFFER_SIZE = 1024


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(BUFFER_SIZE).decode("utf-8")
            if not message:
                print("Disconnected from server")
                break
            print(f"Message from server: {message}")
        except Exception as e:
            print(f"Error: {e}")
            break

    sock.close()


def main(server_ip, port, role):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    client_socket.send(role.encode("utf-8"))

    if role == "SUBSCRIBER":
        thread = threading.Thread(target=receive_messages, args=(client_socket,))
        thread.start()

    while True:
        message = input()
        client_socket.send(message.encode("utf-8"))
        if message == "terminate":
            print("Terminate command sent. Disconnecting from server.")
            break

    client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <SERVER_IP> <PORT> <ROLE>")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    role = sys.argv[3]

    if role not in ["PUBLISHER", "SUBSCRIBER"]:
        print("Role must be either 'PUBLISHER' or 'SUBSCRIBER'")
        sys.exit(1)

    main(server_ip, port, role)
