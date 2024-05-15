from socket import *
import packet
import struct
import random
import time

window_size = 4
timeout_seconds = 1


def read_image_binary(image_path):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    return image_data


def send(filename, receiver_ip, receiver_port, max_segment_size, window_size, file_id):
    window_start = 0
    window_end = 0

    # Read the file
    image_data = read_image_binary(filename)
    packets = packet.create_data_packets(image_data, max_segment_size, file_id)
    total_packets = len(packets)
    acks_received = [False] * total_packets

    with socket(AF_INET, SOCK_DGRAM) as sender:
        sender.settimeout(timeout_seconds)
        while window_start < total_packets:
            # Send packets in the current window range
            for i in range(window_start, min(window_start + window_size, total_packets)):
                if not acks_received[i]:
                    if random.randint(1, 100) >= 15:  # 15% packet loss
                        sender.sendto(packets[i].packet, (receiver_ip, receiver_port))
                        print(f"Sent packet with id {packets[i].packet_id}, file id {packets[i].file_id}")

            # Listen for acknowledgments
            try:
                while True:
                    ack_packet, _ = sender.recvfrom(4096)
                    ack_packet_id = struct.unpack('!H', ack_packet[:2])[0]
                    print(f"Received ack for packet id {ack_packet_id}")
                    if ack_packet_id < total_packets:
                        acks_received[ack_packet_id] = True
                        if ack_packet_id == window_start:
                            while window_start < total_packets and acks_received[window_start]:
                                window_start += 1

            except timeout:
                pass

        print(f"Image {filename} sent")


# Sending all images sequentially
imgs = ['large', 'medium', 'small']
for index, img in enumerate(imgs, start=1):
    send(f"images\\{img}.jpeg", '127.0.0.1', 12345, 1024, 5, index)
