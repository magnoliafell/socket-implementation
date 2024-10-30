import socket
import threading
from encryption import decrypt, encrypt

clients = {}
key = "12345678"

def handle_client(conn, address, key):
    client_id = f"{address[0]}:{address[1]}"
    clients[client_id] = conn
    print("Connection from:", client_id)

    while True:
        try:
            # Receive and decrypt data from the client
            encrypted_data = conn.recv(1024)
            if not encrypted_data:
                break

            # Decrypt the message
            decrypt_message = decrypt(encrypted_data.decode(), key)

            # Check if the message is directed to a specific client
            if decrypt_message.startswith("@"):
                # Extract target client ID and the actual message
                target_id, message = decrypt_message[1:].split(" ", 1)

                # Check if target client exists
                if target_id in clients:
                    msg = f"[{client_id}] {message}"
                    encrypt_msg = encrypt(msg, key)  # Encrypt the message
                    clients[target_id].send(encrypt_msg.encode())  # Send encrypted message
                    print(f"from {client_id} {encrypt_msg}")  # Print the encrypted message
                else:
                    print(f"Target client {target_id} not connected.")
            else:
                print(f"Unable to determine address: {decrypt_message}")

        except Exception as e:
            print(f"Error with {client_id}: {e}")
            break

    # Close connection and remove client from dictionary
    conn.close()
    del clients[client_id]
    print(f"Connection closed from: {client_id}")

# Function to start the server
def server_program(key):
    port = 5050
    host = socket.gethostname()
    addr = (host, port)

    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(4)

    print("Server is running... Waiting for connections...")
    while True:
        conn, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")

        # Start a new thread to handle each client
        client_thread = threading.Thread(target=handle_client, args=(conn, addr, key))
        client_thread.start()

# Main program to initialize server with encryption key
if __name__ == '__main__':
    server_program(key)
