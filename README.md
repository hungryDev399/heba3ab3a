# heba3ab3a

# Reliable Image Transfer Protocol

A lightweight, UDP-based file transfer protocol with a sliding window mechanism to ensure reliable delivery of images over a network with simulated packet loss.

## Features
- **Reliable Transmission:** Implements a sliding window protocol with selective repeat to ensure reliable and ordered delivery of image packets.
- **Packet Loss Simulation:** Simulates packet loss with a configurable percentage.
- **Multiple Image Transfer:** Supports sequential transfer of multiple files from the sender to the receiver.
- **Acknowledgment-Based:** Uses acknowledgment packets to confirm receipt of individual data packets.

## Files and Structure
- `packet.py`: Contains the definitions for data and acknowledgment packets, and functions to create data packets.
- `sender.py`: The sender side of the protocol that reads images from disk, breaks them into packets, and sends them to the receiver.
- `receive.py`: The receiver side of the protocol that listens for packets, acknowledges them, and reconstructs the image files.

### File Structure
```
.
├── images
│   ├── large.jpeg
│   ├── medium.jpeg
│   └── small.jpeg
├── packet.py
├── sender.py
└── receive.py
```

## Usage

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/reliable-image-transfer.git
cd reliable-image-transfer
```

### 2. Prepare Images
Place your images in the `images` directory and ensure they are named according to the `imgs` list in `sender.py`.

### 3. Run the Receiver
Start the receiver to listen for incoming packets.
```bash
python receive.py
```

### 4. Run the Sender
Start the sender to send images sequentially to the receiver.
```bash
python sender.py
```

## Configuration
- **Packet Loss Simulation:** The sender simulates a 15% packet loss by default. You can adjust this by changing the probability condition in the `send` function of `sender.py`.

```python
if random.randint(1, 100) >= 15:  # Adjust this value for different loss rates
    sender.sendto(packets[i].packet, (receiver_ip, receiver_port))
```

- **Sliding Window Size:** The window size is adjustable in `sender.py` through the `window_size` parameter.

```python
window_size = 4  # Adjust the size as needed
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

To use this README effectively, save it as a `README.md` file in the root of your GitHub repository. Make sure to adjust the image paths and file names accordingly.
