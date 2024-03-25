import re

def analyze_log(file_path):
    connections = {}
    packet_sizes = []

    with open(file_path, 'r') as file:
        for line in file:
            # Extract client address, sequence number, packet size, and message chunk from each log line
            match = re.search(r"From \('(.+?)', (\d+)\) - Seq: (\d+), Size: (\d+) bytes, Chunk: '(.+?)'", line)
            if match:
                addr = match.group(1)
                port = int(match.group(2))
                seq_num = int(match.group(3))
                size = int(match.group(4))
                chunk = match.group(5)

                # Record packet size
                packet_sizes.append(size)

                # Initialize or update connection info
                if (addr, port) not in connections:
                    connections[(addr, port)] = {'packets': 1, 'total_size': size}
                else:
                    connections[(addr, port)]['packets'] += 1
                    connections[(addr, port)]['total_size'] += size

    # Display statistics
    print("Connection Stats:")
    for (addr, port), stats in connections.items():
        print(f"  {addr}:{port} -> Packets: {stats['packets']}, Total Size: {stats['total_size']} bytes")

    avg_packet_size = sum(packet_sizes) / len(packet_sizes) if packet_sizes else 0
    print(f"\nAverage Packet Size: {avg_packet_size:.2f} bytes")

if __name__ == '__main__':
    log_file_path = 'server_log.txt'  # Path to your server log file
    analyze_log(log_file_path)
