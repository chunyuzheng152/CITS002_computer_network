#layer 4
class Host:
    def send_data(self, dst_ip, data, network):
        pass

    def receive_segment(self, segment, src_ip, network):
        pass
    
#layer 2&3
class Host:
    def __init__(self, name, ip, mac):
        pass

    def send_segment(self, dst_ip, segment, network):
        pass

    def receive_frame(self, frame, network):
        pass

    def receive_packet(self, packet, network):
        pass


class Router:
    def __init__(self, name):
        pass

    def receive_frame(self, frame, incoming_interface, network):
        pass

    def forward_packet(self, packet, incoming_interface, network):
        pass