import socket

def send_message(server_addr, message, buffer_size=4096, timeout=2):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        seq_num = 0
        message += '\n'

        for i in range(0, len(message), buffer_size - 2):
            chunk = message[i:i + buffer_size - 2]
            data = f'{seq_num:02}'.encode() + chunk.encode()

            while True:
                try:
                    sock.sendto(data, server_addr)
                    ack_data, _ = sock.recvfrom(buffer_size)
                    ack_seq_num = int(ack_data.decode().replace('ACK', ''))
                    if ack_seq_num == seq_num:
                        break
                except socket.timeout:
                    continue
            seq_num += 1

        reversed_message = receive_reversed_message(sock, seq_num, buffer_size, server_addr)
        print(f"Reversed message: '{reversed_message}'")

def receive_reversed_message(sock, start_seq_num, buffer_size, server_addr):
    reversed_message = ''
    seq_num = start_seq_num

    while True:
        #print("Receiving data1")
        try:
            data, _ = sock.recvfrom(buffer_size)
            if len(data) >= 3:
                char_seq_num = int(data[:2])
                chunk = data[2:].decode()
                #print("Received data2: ", chunk, char_seq_num, seq_num)
                if True:
                    if chunk.endswith('\n'):
                        reversed_message += chunk[:-1]  # Remove the last '\n'
                        break
                    #print("Received chunk3: ", chunk)
                    reversed_message += chunk
                    ack = f'ACK{char_seq_num:02}'.encode()
                    sock.sendto(ack, server_addr)
                    seq_num += 1
        except socket.timeout:
            break

    return reversed_message

if __name__ == '__main__':
    server_address = ('localhost', 12349)
    message = input("Enter a message to send: ")
    send_message(server_address, message)
