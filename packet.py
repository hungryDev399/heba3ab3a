import struct


def create_data_packets(data, max_segment_size, file_id):
    packets = []
    packet_id = 0
    # the leftover of the mss after removing metadata
    max_data_size = max_segment_size - 16 - 16 - 32
    data_left = len(data)
    # to make sure there is at least one bit left for special the last packet
    for i in range(0, len(data) - max_data_size, max_data_size):
        packet_data = data[i:i + max_data_size]
        packets.append(Packet(packet_id, packet_data, file_id))
        packet_id += 1

    # create the last packet with the remaining data
    packets.append(
        Packet(packet_id, data[packet_id * max_data_size:], file_id, True))
    return packets


class Packet:
    def __init__(self, packet_id, data, file_id, is_last=False):
        self.packet_id = packet_id
        self.data = data if isinstance(data, bytes) else data.encode()
        self.trailer = 0x00000000 if not is_last else 0xFFFFFFFF
        self.file_id = file_id
        self.packet = struct.pack('!HH{}sI'.format(
            len(self.data)), packet_id, file_id, self.data, self.trailer)

    def from_binary(data):
        packet_id, file_id, packet_data, trailer = struct.unpack(
            '!HH{}sI'.format(len(data) - 8), data)
        return Packet(packet_id, packet_data, file_id, trailer == 0xFFFFFFFF)


class AckPacket:
    def __init__(self, packet_id):
        self.packet_id = packet_id
        self.packet = struct.pack('!H', packet_id)
