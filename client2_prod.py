import socket

def send_message(server_addr, message, buffer_size=1024, timeout=2):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        seq_num = 0
        message += '\n'  # Signify the end of the message

        # Sending each character of the message with a sequence number
        for char in message:
            data = f'{char}{seq_num:02}'.encode()
            while True:
                try:
                    sock.sendto(data, server_addr)
                    ack_data, _ = sock.recvfrom(buffer_size)
                    ack_seq_num = int(ack_data.decode().replace('ACK', ''))
                    if ack_seq_num == seq_num:
                        break  # Move to the next character once acknowledgment is received
                except socket.timeout:
                    continue  # Resend the character if timeout occurs
            seq_num += 1  # Increment the sequence number for the next character

        # Receiving and assembling the reversed message from the server
        reversed_message = receive_reversed_message(sock, seq_num, buffer_size, server_addr)
        print(f"Reversed message: '{reversed_message}'")

def receive_reversed_message(sock, start_seq_num, buffer_size, server_addr):
    reversed_message = ''
    seq_num = start_seq_num

    while True:
        try:
            data, _ = sock.recvfrom(buffer_size)
            if len(data) >= 3:  # Check for at least 1 char and 2 digits of seq_num
                #print(data)
                char, char_seq_num = data[:-2].decode(), int(data[-2:])
                #print(char, char_seq_num, seq_num)
                if True:  # Process only if seq_num matches expected
                    #print(char)
                    if char == '\n':  # Check for end-of-message character
                        break  # Complete message received
                    reversed_message += char  # Append the received character
                    #print(reversed_message)
                    #print(char)
                    ack = f'ACK{char_seq_num:02}'.encode()
                    sock.sendto(ack, server_addr)  # Acknowledge the received character
                    seq_num += 1  # Increment for the next expected character
        except socket.timeout:
            break  # End the loop if no more data is received

    return reversed_message  # Return the fully assembled reversed message

if __name__ == '__main__':
    server_address = ('localhost', 12347)
    message = input("Enter a message to send: ")
    send_message(server_address, message)