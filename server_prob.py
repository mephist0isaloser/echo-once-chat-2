import socket
import threading

def client_handler(client_addr, server_sock, buffer_size=1024):
    message_buffer = []
    expected_seq_num = 0

    while True:
        data, addr = server_sock.recvfrom(buffer_size)
        if addr == client_addr:
            char, seq_num = parse_data(data)

            if seq_num == expected_seq_num:
                print(f"Received '{char}' with seq_num {seq_num} from {addr}")
                message_buffer.append(char)
                ack = f'ACK{seq_num:02}'.encode()
                server_sock.sendto(ack, client_addr)

                if char == '\n':
                    message = ''.join(message_buffer[:-1])
                    reversed_message = reverse_and_respond(message)

                    for idx, char in enumerate(reversed_message + '\n'):  # Include '\n' in enumeration
                        send_char_with_seq(server_sock, char, expected_seq_num, client_addr)
                        expected_seq_num += 1  # Increment after sending each char of reversed message

                    message_buffer = []
                    expected_seq_num = 0
                    break  # Exit the loop after sending the full reversed message
                else:
                    expected_seq_num += 1

def parse_data(data):
    char = data[:-2].decode()
    seq_num = int(data[-2:])
    return char, seq_num

def reverse_and_respond(message):
    return message[::-1]

def send_char_with_seq(sock, char, seq_num, client_addr):
    data = f'{char}{seq_num:02}'.encode()
    sock.sendto(data, client_addr)

def start_server(host='localhost', port=12347, buffer_size=1024):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_sock:
        server_sock.bind((host, port))
        print(f"Server started at {host}:{port}")

        while True:
            data, client_addr = server_sock.recvfrom(buffer_size)
            threading.Thread(target=client_handler, args=(client_addr, server_sock, buffer_size)).start()

if __name__ == '__main__':
    start_server()