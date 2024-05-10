# Project Implementation Plan: Reliable Transport Protocol (Go-Back-N)

## Requirements:

### 1. File Chunking and Packet Creation:

The sender should read a file and divide it into chunks with size ≤ Maximum Segment Size (MSS). Each chunk is encapsulated into a packet with:

- **Packet ID (16 bits):** Unique identifier for each packet.
- **File ID (16 bits):** Unique identifier for the file.
- **Application Data:** The chunk of data.
- **Trailer (32 bits):** 0x0000 for all but the last packet (0xFFFF).

### 2. Reliable Data Transfer with Go-Back-N:

Implement Go-Back-N (GBN) protocol over UDP. Sender maintains a sliding window of size N (maximum unacknowledged packets). On receiving acknowledgement, slide the window and send new packets within the window. On packet timeout, retransmit all packets in the current window.

### 3. Acknowledgement Mechanism:

Receiver sends acknowledgement packets with:

- **File ID (16 bits):** ID of the file.
- **Packet ID (16 bits):** ID of the last correctly received packet (cumulative acknowledgement).

### 4. Simulated Packet Loss:

Simulate packet loss at receiver with a loss rate between 5% and 15%.

### 5. File Writing:

Receiver writes received data to a new file upon receiving the last packet.

## Implementation Steps:

### Requirement 1: File Chunking and Packet Creation

- **File Reading:** Use file I/O functions to open and read the file content.
- **Chunking:** Divide file content into chunks ≤ MSS.
- **Packet Creation:**
  - Define a data structure for the packet format.
  - Implement a function to create a packet with header and trailer from a data chunk.
  - Generate unique Packet IDs.

### Requirement 2: Reliable Data Transfer with Go-Back-N

- **Sliding Window:** Create a data structure to represent the sliding window with base and end.
- **Packet Sending:** Use UDP sockets to send packets; send initial window (N packets).
- **Acknowledgement Handling:**
  - On receiving ACK, extract Packet ID.
  - If acknowledged Packet ID > window base, slide the window and send new packets.
- **Timeout and Retransmission:**
  - Implement a timer for each unacknowledged packet.
  - On timeout, retransmit all packets in the current window.

### Requirement 3: Acknowledgement Mechanism

- **Acknowledgement Packet Creation:** Define a data structure for the ACK message format.
- **Acknowledgement Sending:** Use UDP sockets to send ACK messages after receiving a packet.

### Requirement 4: Simulated Packet Loss

- **Random Packet Drop:**
  - For each received packet, generate a random number.
  - Discard the packet if the number is less than the loss rate.
  - Otherwise, process the packet and send an acknowledgement.

### Requirement 5: File Writing

- **File Writing:**
  - Store received data in a buffer.
  - On receiving the last packet (0xFFFF trailer), write buffered data to a new file.
