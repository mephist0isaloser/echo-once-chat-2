import socket
from server_prod import PORT  # Import the PORT variable from the server script


def send_message(server_addr, message, buffer_size=4096, timeout=2):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        seq_num = 0
        message += '\n'

        for i in range(0, len(message), buffer_size - 2):
            chunk = f'{seq_num:02}{message[i:i + buffer_size - 2]}'
            while True:
                try:
                    sock.sendto(chunk.encode(), server_addr)
                    ack_data, _ = sock.recvfrom(1024)  # Smaller buffer size for ACKs
                    ack_seq_num = int(ack_data.decode().replace('ACK', ''))
                    if ack_seq_num == seq_num:
                        break
                except socket.timeout:
                    continue
            seq_num += 1

        reversed_message = ''
        while True:
            try:
                data, _ = sock.recvfrom(buffer_size)
                if len(data) >= 3:
                    char_seq_num = int(data[:2])
                    chunk = data[2:].decode()

                    if chunk.endswith('\n'):
                        reversed_message += chunk[:-1]
                        break
                    reversed_message += chunk
                    ack = f'ACK{char_seq_num:02}'.encode()
                    sock.sendto(ack, server_addr)
                    seq_num += 1
            except socket.timeout:
                break

        return reversed_message


if __name__ == '__main__':
    server_address = ('localhost', PORT)

    while True:
        message = input("Enter a message to send (or type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        reversed_message = send_message(server_address, message)
        print(f"Reversed message: '{reversed_message}'")
