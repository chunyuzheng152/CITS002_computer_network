# protocol.py


# Person A writes this class: Layer 4 UDP-like segment.
class Segment:
    def __init__(self, src_port, dst_port, data, seg_type, seq_num):
        self.src_port = src_port
        self.dst_port = dst_port
        self.data = data
        self.type = seg_type
        self.seq_num = seq_num
        self.length = 10 + len(data)
        self.checksum = self.calculate_checksum()

    def calculate_checksum(self):
        total = 0
        text = str(self.src_port) + str(self.dst_port) + self.data + str(self.type) + str(self.seq_num)
        for char in text:
            total += ord(char)
        return total % 256

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