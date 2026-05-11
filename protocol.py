# protocol.py
import struct

# Person A writes this class: Layer 4 UDP-like segment.
class Segment:
    def __init__(self, src_port, dst_port, seg_type, seq_num, data=""):
        self.src_port = src_port    # 2 bytes
        self.dst_port = dst_port    # 2 bytes
        self.seg_type = seg_type        # 1 byte(0:DATA, 1:ACK)
        self.seq_num = seq_num          # 1 byte(0 or 1)
        self.data = data                # variable length
        self.length = 10 + len(data)    # 2 bytes

        self.checksum = 0
        self.checksum = self.calculate_checksum()

    def calculate_checksum(self):
        format_string = "!HHHHBB"
        header_bytes = struct.pack(format_string, self.src_port, self.dst_port, self.length, 0, self.seg_type, self.seq_num)
        total = sum(header_bytes) + sum(self.data.encode('utf-8'))
        return total % 65536

    def verify_checksum(self):
        return self.checksum == self.calculate_checksum()


class Packet:
    def __init__(self, src_ip, dst_ip, ttl, protocol, payload):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.ttl = ttl
        self.protocol = protocol
        self.payload = payload
        self.total_length = 12 + payload.length

    def decrement_ttl(self):
        self.ttl -= 1
        return self.ttl

class Frame:
    def __init__(self, src_mac, dst_mac, eth_type, payload):
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.eth_type = eth_type
        self.payload = payload