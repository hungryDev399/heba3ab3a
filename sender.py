import datetime
from socket import *
import packet
import struct
import random
import time
import matplotlib.pyplot as plt

window_size = 4
timeout_seconds = 0.5
packet_loss_rate = 0.15  # 15% packet loss


def read_image_binary(image_path):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    return image_data


def plot_packet_transmissions(packet_logs, retransmissions, filename, window_size, timeout_seconds, packet_loss_rate, start_time, end_time, total_packets, total_bytes):
    packet_ids = [log[0] for log in packet_logs]
    timestamps = [log[1] for log in packet_logs]
    retransmitted_ids = [log[0] for log in retransmissions]
    retransmitted_times = [log[1] for log in retransmissions]

    plt.figure(figsize=(10, 6))
    plt.scatter(timestamps, packet_ids, color='blue', label='Sent Packets')
    plt.scatter(retransmitted_times, retransmitted_ids,
                color='red', label='Retransmitted Packets')
    plt.xlabel('Time (s)')
    plt.ylabel('Packet ID')
    plt.title(
        f'Packet ID vs. Time (File: {filename})\n'
        f'Window Size: {window_size}, Timeout: {
            timeout_seconds}s, Loss Rate: {int(packet_loss_rate * 100)}%\n'
        f'Start Time: {start_time}, End Time: {
            end_time}, Elapsed Time: {end_time - start_time}\n'
        f'Total Packets: {total_packets}, Total Bytes: {
            total_bytes}, Retransmissions: {len(retransmissions)}\n'
        f'Average Transfer Rate: {total_bytes / (end_time - start_time).total_seconds(
        )} bytes/sec, {total_packets / (end_time - start_time).total_seconds()} packets/sec'
    )
    plt.legend()
    plt.grid(True)
    plt.show()


def send(filename, receiver_ip, receiver_port, max_segment_size, window_size, file_id):
    window_start = 0

    image_data = read_image_binary(filename)
    packets = packet.create_data_packets(image_data, max_segment_size, file_id)
    total_packets = len(packets)
    total_bytes = sum([len(p.packet) for p in packets])
    acks_received = [False] * total_packets
    packet_logs = []
    retransmissions = []

    start_time = datetime.datetime.now()

    with socket(AF_INET, SOCK_DGRAM) as sender:
        sender.settimeout(timeout_seconds)
        while window_start < total_packets:
            for i in range(window_start, min(window_start + window_size, total_packets)):
                if not acks_received[i]:
                    timestamp = time.time()
                    if random.random() >= packet_loss_rate:
                        sender.sendto(packets[i].packet,
                                      (receiver_ip, receiver_port))
                        packet_logs.append((packets[i].packet_id, timestamp))
                        print(f"Sent packet with id {
                              packets[i].packet_id}, file id {packets[i].file_id} at time {datetime.datetime.now()}")

            # wait for acknowledgments
            try:
                while not all(acks_received[window_start:window_start + window_size]):
                    ack_packet, _ = sender.recvfrom(4096)
                    ack_packet_id = struct.unpack('!H', ack_packet[:2])[0]
                    print(f"Received ack for packet id {
                          ack_packet_id} at time {datetime.datetime.now()}")
                    if ack_packet_id == window_start:
                        acks_received[ack_packet_id] = True
                        if ack_packet_id == window_start:
                            while window_start < total_packets and acks_received[window_start]:
                                window_start += 1
                continue

            except timeout:
                # retransmit packets in the window
                for i in range(window_start, min(window_start + window_size, total_packets)):
                    if not acks_received[i]:
                        timestamp = time.time()
                        sender.sendto(packets[i].packet,
                                      (receiver_ip, receiver_port))
                        retransmissions.append(
                            (packets[i].packet_id, timestamp))
                        print(f"Retransmitting packet with id {
                              packets[i].packet_id} at time {datetime.datetime.now()}")

                        # wait for acknowledgments after retransmission
                try:
                    while not all(acks_received[window_start:window_start + window_size]):
                        ack_packet, _ = sender.recvfrom(4096)
                        ack_packet_id = struct.unpack(
                            '!H', ack_packet[:2])[0]
                        print(f"Received ack for packet id {
                              ack_packet_id} at time {datetime.datetime.now()}")
                        if ack_packet_id == window_start:
                            acks_received[ack_packet_id] = True
                            if ack_packet_id == window_start:
                                while window_start < total_packets and acks_received[window_start]:
                                    window_start += 1
                    continue

                except timeout:
                    continue

        end_time = datetime.datetime.now()

        print(f"Image {filename} sent at time {datetime.datetime.now()}")
        plot_packet_transmissions(packet_logs, retransmissions, filename, window_size,
                                  timeout_seconds, packet_loss_rate, start_time, end_time, total_packets, total_bytes)


# Send images
imgs = ['large', 'medium', 'small']
# imgs = ['small']
for index, img in enumerate(imgs, start=1):
    send(f"images/{img}.jpeg", '127.0.0.1', 12345, 1024, 5, index)
