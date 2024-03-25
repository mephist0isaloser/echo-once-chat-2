import socket
import threading
#from main import PORT  # Import the PORT variable from
# Global set to keep track of active client addresses
PORT = 39629
active_clients = set()

def client_handler(client_addr, server_sock, buffer_size=4096):
    global active_clients

    print(f"Connected to client: {client_addr}")
    message_buffer = []
    expected_seq_num = 0

    while True:
        data, addr = server_sock.recvfrom(buffer_size)
        if addr == client_addr:
            # Check if the packet is an ACK packet
            if data.startswith(b'ACK'):
                continue  # Ignore ACK packets, no further processing required

            try:
                seq_num = int(data[:2])
                message_chunk = data[2:].decode()

                if seq_num == expected_seq_num:
                    print(f"From {addr} - Seq: {seq_num}, Size: {len(data)} bytes, Chunk: '{message_chunk}'")
                    message_buffer.append(message_chunk)
                    ack = f'ACK{seq_num:02}'.encode()
                    server_sock.sendto(ack, client_addr)

                    if message_chunk.endswith('\n'):
                        message = ''.join(message_buffer)[:-1]  # Remove the newline character
                        reversed_message = message[::-1]

                        for idx, char in enumerate(reversed_message + '\n'):
                            chunk = f'{expected_seq_num:02}{char}'.encode()
                            server_sock.sendto(chunk, client_addr)
                            expected_seq_num += 1

                        message_buffer = []
                        expected_seq_num = 0
                        break  # End the client handler loop after sending the reversed message
            except ValueError as e:
                print(f"Error processing packet from {addr}: {e}")

    with threading.Lock():
        if client_addr in active_clients:
            active_clients.remove(client_addr)

def start_server(host='localhost', port=PORT, buffer_size=4096):
    global active_clients

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_sock:
        server_sock.bind((host, port))
        print(f"Server started at {host}:{port}")

        while True:
            data, client_addr = server_sock.recvfrom(1024)  # Initial packet size for client detection
            with threading.Lock():
                if client_addr not in active_clients:
                    active_clients.add(client_addr)
                    threading.Thread(target=client_handler, args=(client_addr, server_sock, buffer_size)).start()

if __name__ == '__main__':
    start_server()
