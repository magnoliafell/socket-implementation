import socket
import threading
from encryption import encrypt, decrypt

key = "12345678"

def receive_messages(conn, key):
    while True:
        try:
            encrypted_data = conn.recv(1024)
            if not encrypted_data:
                print("Disconnected from server")
                break
            decrypted_message = decrypt(encrypted_data.decode(), key)
            print(f"{decrypted_message}")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def client_program():
    port = 5050
    host = socket.gethostname()
    addr = (host, port)

    client_socket = socket.socket()
    client_socket.connect(addr)

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, key))
    receive_thread.start()

    print("Connected to the server. Type '@client_id message' to send a message to another client.")

    while True:
        try:
            message = input(" -> ")
            if message.lower() == "exit":
                break
            encrypted_message = encrypt(message, key)
            client_socket.send(encrypted_message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")
            break

    client_socket.close()

if __name__ == "__main__":
    client_program()
