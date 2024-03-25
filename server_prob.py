import socket
import threading

def client_handler(client_addr, server_sock, buffer_size=4096):
    message_buffer = []
    expected_seq_num = 0

    while True:
        data, addr = server_sock.recvfrom(buffer_size)
        if addr == client_addr:
            message_chunk, seq_num = parse_data(data)

            if seq_num == expected_seq_num:
                print(f"Received message chunk with seq_num {seq_num} from {addr}")
                message_buffer.append(message_chunk)
                ack = f'ACK{seq_num:02}'.encode()
                server_sock.sendto(ack, client_addr)

                if message_chunk.endswith('\n'):
                    message = ''.join(message_buffer)[:-1]  # Remove the last '\n'
                    reversed_message = reverse_and_respond(message)

                    send_in_chunks(server_sock, reversed_message, expected_seq_num, client_addr, buffer_size)
                    break

                expected_seq_num += 1

def parse_data(data):
    seq_num = int(data[:2])
    message_chunk = data[2:].decode()
    return message_chunk, seq_num

def reverse_and_respond(message):
    return message[::-1]

def send_in_chunks(sock, message, seq_num, client_addr, buffer_size):
    for i in range(0, len(message), buffer_size - 2):
        chunk = message[i:i + buffer_size - 2]
        data = f'{seq_num:02}'.encode() + chunk.encode()
        sock.sendto(data, client_addr)
        seq_num += 1
    # Send end-of-message marker
    sock.sendto(f'{seq_num:02}\n'.encode(), client_addr)

def start_server(host='localhost', port=12349, buffer_size=4096):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_sock:
        server_sock.bind((host, port))
        print(f"Server started at {host}:{port}")

        while True:
            data, client_addr = server_sock.recvfrom(buffer_size)
            threading.Thread(target=client_handler, args=(client_addr, server_sock, buffer_size)).start()

if __name__ == '__main__':
    start_server()
