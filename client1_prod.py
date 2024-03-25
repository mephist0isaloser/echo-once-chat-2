import socket
from server_prod import PORT  # Import the PORT variable from the server script

def send_message(server_addr, message, buffer_size=4096, timeout=2):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        seq_num = 0
        message += '\n'  # Append newline as an end-of-message marker

        # Adjusted buffer size to accommodate typical MTU size while leaving room for headers
        optimal_chunk_size = 1472  # 1500 (common MTU size) - 20 (IP header) - 8 (UDP header)

        # Send the message in chunks to reduce overhead
        for i in range(0, len(message), optimal_chunk_size - 2):
            chunk = f'{seq_num:02}{message[i:i + optimal_chunk_size - 2]}'
            while True:
                try:
                    # Send each chunk to the server
                    sock.sendto(chunk.encode(), server_addr)
                    # Wait for an acknowledgment before sending the next chunk
                    ack_data, _ = sock.recvfrom(1024)  # Using a smaller buffer size for ACK packets
                    ack_seq_num = int(ack_data.decode().replace('ACK', ''))
                    if ack_seq_num == seq_num:
                        break  # Move to the next chunk if the correct ACK is received
                except socket.timeout:
                    continue  # Retry sending the chunk if a timeout occurs
            seq_num += 1  # Increment sequence number for the next chunk

        # Reassemble the reversed message received from the server
        reversed_message = ''
        while True:
            try:
                data, _ = sock.recvfrom(buffer_size)
                if len(data) >= 3:
                    char_seq_num = int(data[:2])
                    chunk = data[2:].decode()

                    if chunk.endswith('\n'):  # Check for end-of-message marker
                        reversed_message += chunk[:-1]  # Exclude the newline marker from the final message
                        break  # End the loop as the complete message has been received
                    reversed_message += chunk  # Append received chunk to the reversed message

                    # Acknowledge the receipt of each chunk
                    ack = f'ACK{char_seq_num:02}'.encode()
                    sock.sendto(ack, server_addr)
                    seq_num += 1  # Prepare for the next chunk
            except socket.timeout:
                break  # Stop waiting for more data if a timeout occurs

        return reversed_message  # Return the assembled reversed message

if __name__ == '__main__':
    server_address = ('localhost', PORT)

    # Continuously read messages from the user and send them to the server for reversal
    while True:
        message = input("Enter a message to send (or type 'exit' to quit): ")
        if message.lower() == 'exit':
            break  # Exit the loop and terminate the client if the user types 'exit'
        reversed_message = send_message(server_address, message)  # Send the message and receive the reversed version
        print(f"Reversed message: '{reversed_message}'")  # Print the reversed message
