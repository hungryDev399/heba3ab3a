from socket import *

import packet
import struct


def read_image_binary(image_path):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    return image_data


def send(filename, receiver_ip, receiver_port, max_segment_size, window_size_n):
    # read the file
    image_data = read_image_binary(filename)
    file_id = 2

    packets = packet.create_data_packets(image_data, max_segment_size, file_id)
    # create the udp socket
    with socket(AF_INET, SOCK_DGRAM) as sender:
        for i in range(0, len(packets)):
            sender.sendto(packets[i].packet, (receiver_ip, receiver_port))
            print(f'sent packet with id {
                  struct.unpack("!h", packets[i].packet[:2])[0]}')

        print('image sent')


send('images\\large.jpeg', '127.0.0.1', 12345, 1024, 5)
