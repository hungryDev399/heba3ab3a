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
