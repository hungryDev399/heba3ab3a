import socket
import struct
import packet
import datetime


def reconstruct_image(data, output_filename):
    with open(output_filename, 'wb') as f:
        f.write(data)


def receive_packets(ip_address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (ip_address, port)
    sock.bind(server_address)

    def receive_file():
        data = {}
        last_id = -1
        expected_id = 0
        file_id = 0
        while True:
            packet_binary, addr = sock.recvfrom(4096)
            received_packet = packet.Packet.from_binary(packet_binary)

            print(f"Received packet with id {
                  received_packet.packet_id} from {addr} at time {datetime.datetime.now()}")

            if received_packet.packet_id == expected_id:
                data[received_packet.packet_id] = received_packet.data
                last_id = received_packet.packet_id
                expected_id += 1
                file_id = received_packet.file_id

                # accept subsequent packets if already received
                while expected_id in data:
                    expected_id += 1
            else:
                data[received_packet.packet_id] = received_packet.data

            ack_packet = packet.AckPacket(received_packet.packet_id).packet
            sock.sendto(ack_packet, addr)
            print(f"Sent ack for packet id {
                  received_packet.packet_id} at time {datetime.datetime.now()}")

            if received_packet.trailer == 0xFFFFFFFF:
                break

        # reconstruct the image
        sorted_data = b''.join(data[i] for i in sorted(data.keys()))
        reconstruct_image(sorted_data, f'images\\received_{file_id}.jpeg')

    # receive the three files
    for _ in range(3):
        receive_file()


ip_address = '127.0.0.1'
port = 12345

receive_packets(ip_address, port)
