import socket
import struct
import packet


def reconstruct_image(data, output_filename):
    with open(output_filename, 'wb') as f:
        f.write(data)


def receive_packets(ip_address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (ip_address, port)
    sock.bind(server_address)

    data = b''
    while True:
        packet_rec, addr = sock.recvfrom(4096)  # buffer size is 4096 bytes
        print(f"received packet from {addr} of size {
              len(packet_rec)} with id {struct.unpack('!H', packet_rec[:2])[0]}")
        # send an ack
        ack_packet = packet.AckPacket(packet_rec).packet
        sock.sendto(ack_packet, addr)
        print(f"sent ack to {addr}")
        # append each packet after removing its metadata
        data += packet_rec[4:-4]
        # get the last 4 bytes of the packet
        last_32_bits = struct.unpack('!I', packet_rec[-4:])[0]

        if last_32_bits == 0xFFFFFFFF:
            # get the file id
            file_id = packet_rec[:2][0]
            break

    # ceconstruct the image
    reconstruct_image(data, f'images\\received_{file_id}.jpeg')


ip_address = '127.0.0.1'
port = 12345

receive_packets(ip_address, port)
