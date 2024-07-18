import socket
import sys
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            break

def start_client(server_ip, server_port, role, topic):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    client_socket.send(f"{role} {topic}".encode())

    print(f"Connected to server at {server_ip}:{server_port} as {role} on topic {topic}")

    if role == "SUBSCRIBER":
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

    while True:
        if role == "PUBLISHER":
            message = input("Enter message (type 'terminate' to quit): ")
            client_socket.send(message.encode())
            if message.lower() == "terminate":
                print("Terminating connection")
                client_socket.close()
                break
        else:
            # Subscribers do not send messages; they only receive.
            pass

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python client.py <server_ip> <server_port> <role> <topic>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    role = sys.argv[3].upper()
    topic = sys.argv[4].upper()

    if role not in ["PUBLISHER", "SUBSCRIBER"]:
        print("Role must be either 'PUBLISHER' or 'SUBSCRIBER'")
        sys.exit(1)

    start_client(server_ip, server_port, role, topic)
