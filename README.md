
# Echo-ohce Chat Application

The Echo-ohce chat application leverages UDP to create a lightweight, efficient, and concurrent server-client messaging system. The server reverses any received string from the client and sends it back, demonstrating the power of UDP sockets for real-time communication while ensuring data integrity and order.

## Docker Image for Quick Deployment

Deploy the server effortlessly using our Docker image:

[Docker Image on Docker Hub](https://hub.docker.com/r/mo8isaloser/echo-oncechat2-server)

## Objectives Masterfully Achieved

- **Leveraging UDP Sockets**: Both the client and server are built upon UDP sockets (`socket.socket(socket.AF_INET, socket.SOCK_DGRAM)`), chosen for their low-latency characteristics compared to TCP, making the application ideal for real-time communication where speed is crucial.

- **Guaranteeing Reliability and Order**: Despite UDP's inherent unreliability, we've meticulously implemented a stop-and-wait protocol to mimic TCP's reliability. After transmitting a packet, the client awaits an acknowledgment from the server before proceeding (`ack_data, _ = sock.recvfrom(1024)`), ensuring each packet is received and processed in the order sent.

- **Seamless Handling of Multiple Clients**: Through advanced threading (`threading.Thread(target=client_handler, args=(client_addr, server_sock, buffer_size)).start()`), the server can manage numerous client connections simultaneously. Each client is serviced in a separate thread, allowing for parallel processing and maintaining high responsiveness.

- **Maximizing Transmission Efficiency**: The application shines in its use of batch processing, sending messages in larger chunks rather than individual characters. This significantly reduces the number of packets sent over the network, lowering the protocol overhead and increasing throughput. This approach is not only efficient but also aligns with best practices for network programming.

## Easy Setup Guide

### Server Deployment

1. Ensure Docker is installed on your machine.
2. Fetch the server image:
   ```
   docker pull mo8isaloser/echo-oncechat2-server
   ```
3. Launch the server container on a chosen port:
   ```
   docker run -d -p <YourPort>:5971 mo8isaloser/echo-oncechat2-server
   ```

### Client Configuration

1. Clone this repository to your system.
2. Navigate to the client script's directory.
3. Confirm Python 3.x is installed.
4. Start the client, matching the server's IP and port:
   ```python
   python client_code.py
   ```

### How to Use

- Input a string in the client's console to send to the server.
- The server will reverse the string and return it, displayed on your screen.
- To end the session, type `'exit'`.

## Deep Dive into Implementation

- **Stop-and-Wait Protocol**: This mechanism is a cornerstone of our reliability strategy, ensuring each piece of data is acknowledged before the next is sent, thus emulating TCP's reliable data transfer over a UDP foundation.

- **Batch Processing**: By intelligently batching data, we significantly reduce the overhead and frequency of UDP packets, aligning with the efficient use of network resources and reducing congestion.

- **Concurrent Client Management**: Our multi-threaded server architecture ensures each client is serviced promptly and independently, showcasing the application's scalability and responsiveness.

Replace `<YourPort>` with your selected port number for the server. Adapt any additional details as necessary for your specific setup.
