# Function Definitions for Go-Back-N Implementation

## 1. `read_file(filename)`

**Parameters:**

- `filename` (string): The path to the file to be read.

**Returns:**

- `data` (bytes): The content of the file as a byte string.

**Functionality:**
Opens the specified file and reads its entire content. Returns the content as a byte string for further processing.

## 2. `create_packet(packet_id, file_id, data, is_last)`

**Parameters:**

- `packet_id` (int): The unique ID for the packet.
- `file_id` (int): The ID of the file to which the packet belongs.
- `data` (bytes): The chunk of data to be included in the packet.
- `is_last` (bool): Indicates whether this is the last packet of the file.

**Returns:**

- `packet` (bytes): The constructed packet as a byte string, including header and trailer information.

**Functionality:**
Creates a packet with the specified format:

- Packet ID (16 bits)
- File ID (16 bits)
- Application Data (variable length)
- Trailer (32 bits, 0x0000 or 0xFFFF based on `is_last`)

## 3. `send_packet(sock, packet, receiver_address)`

**Parameters:**

- `sock` (socket object): The UDP socket object used for sending data.
- `packet` (bytes): The packet data to be sent.
- `receiver_address` (tuple): A tuple containing the receiver's IP address and port number.

**Returns:**

- None

**Functionality:**
Sends the given packet data through the specified UDP socket to the receiver address.

## 4. `receive_packet(sock)`

**Parameters:**

- `sock` (socket object): The UDP socket object used for receiving data.

**Returns:**

- `packet` (bytes): The received packet data as a byte string.
- `sender_address` (tuple): A tuple containing the sender's IP address and port number.

**Functionality:**
Receives data from the specified UDP socket. Returns the received packet data and the address of the sender.

## 5. `parse_packet(packet)`

**Parameters:**

- `packet` (bytes): The received packet data as a byte string.

**Returns:**

- `packet_id` (int): The extracted Packet ID from the packet header.
- `file_id` (int): The extracted File ID from the packet header.
- `data` (bytes): The extracted application data from the packet.
- `is_last` (bool): Indicates whether this is the last packet based on the trailer value.

**Functionality:**
Parses the received packet and extracts the header information (Packet ID, File ID), application data, and trailer value.

## 6. `create_ack(file_id, packet_id)`

**Parameters:**

- `file_id` (int): The ID of the file being acknowledged.
- `packet_id` (int): The ID of the last correctly received packet.

**Returns:**

- `ack_packet` (bytes): The constructed acknowledgement packet as a byte string.

**Functionality:**
Creates an acknowledgement packet with the specified format:

- File ID (16 bits)
- Packet ID (16 bits)

## 7. `is_corrupted(packet)`

**Parameters:**

- `packet` (bytes): The received packet data.

**Returns:**

- `corrupted` (bool): True if the packet is corrupted, False otherwise.

**Functionality:**
Implements a mechanism to check if the received packet is corrupted. This can involve checksum verification or other error detection techniques. In this project, we assume no corruption due to channel errors, so this function can simply return False.

## 8. `write_data_to_file(data, filename)`

**Parameters:**

- `data` (bytes): The data to be written to the file.
- `filename` (string): The name of the file to write the data to.

**Returns:**

- None

**Functionality:**
Writes the given data to the specified file.

## Topological Ordering of Functions:

1. `read_file`
2. `create_packet`
3. `send_packet`
4. `receive_packet`
5. `parse_packet`
6. `is_corrupted`
7. `create_ack`
8. `write_data_to_file`
