from protocol import Packet, Frame, Segment
from config import *

def get_network_for_ip(ip):

    if ip.startswith("10.0.1."):
        return NETWORK_1

    elif ip.startswith("10.0.2."):
        return NETWORK_2

    return None

class Host:
    def __init__(self, name, ip, mac):
        self.name = name
        self.ip = ip
        self.mac = mac

        if self.ip == HOST_A_IP:
            self.routing_table = HOST_A_ROUTING_TABLE
            self.mac_table = HOST_A_MAC_TABLE

        elif self.ip == HOST_B_IP:
            self.routing_table = HOST_B_ROUTING_TABLE
            self.mac_table = HOST_B_MAC_TABLE

        else:
            self.routing_table = {}
            self.mac_table = {}

        self.learned_macs = set()

        self.seq_num = 0
        self.waiting_for_ack = False

        self.expected_seq_num = 0
        self.last_ack_sent = 1


    def send_data(self, dst_ip, data, network):
        print(f"{self.name}: Layer 4: Data received from Application Layer. Data size ={len(data)}")

        chunks = [data[i:i+MAX_SEGMENT_DATA_SIZE] for i in range(0, len(data), MAX_SEGMENT_DATA_SIZE)]

        if not chunks:
            chunks = [""]

        for chunk in chunks:
            self.waiting_for_ack = True

            while self.waiting_for_ack:
                segment = Segment(
                    src_port=SRC_PORT,
                    dst_port=DST_PORT,
                    seg_type=DATA,
                    seq_num=self.seq_num,
                    data=chunk
                )

                print(f"{self.name}: Layer 4: Checksum computed")

                print(f"{self.name}: Layer 4: Segment created by adding transport layer header (DATA, seq={self.seq_num}) (encapsulation)")
                print(f"{self.name}: Layer 4: Segment sent to Network Layer")

                self.send_segment(dst_ip, segment, network)
            self.seq_num = 1 - self.seq_num

    def receive_segment(self, segment, src_ip, network):
        print(f"{self.name}: Layer 4: Segment received from Network Layer")
        
        if not segment.verify_checksum():
            print(f"{self.name}: Layer 4: Segment discarded due to checksum error")

            if segment.seg_type == DATA:
                self.send_ack(src_ip, self.last_ack_sent, network)
            return
        print(f"{self.name}: Layer 4: Checksum verified")

        if segment.seg_type == ACK:
            print(f"{self.name}: Layer 4: ACK received: seq={segment.seq_num}")

            if self.waiting_for_ack and segment.seq_num == self.seq_num:
                self.waiting_for_ack = False
            else:
                print(f"{self.name}: Layer 4: Segment retransmitted due to incorrect ACK")
        
        elif segment.seg_type == DATA:
            if segment.seq_num == self.expected_seq_num:

                print(f"{self.name}: Layer 4: DATA segment delivered to Application Layer. Data size ={len(segment.data)}")
                
                self.send_ack(src_ip, segment.seq_num, network)

                self.last_ack_sent = segment.seq_num
                self.expected_seq_num = 1 - self.expected_seq_num
            else:
                self.send_ack(src_ip, self.last_ack_sent, network)
    
    def send_ack(self, dst_ip, ack_seq_num, network):
        ack_segment = Segment(
            src_port=DST_PORT,
            dst_port=SRC_PORT,
            seg_type=ACK,
            seq_num=ack_seq_num,
            data=""
        )
        print(f"{self.name}: Layer 4: Segment created by adding transport layer header (ACK, seq={ack_seq_num})")
        print(f"{self.name}: Layer 4: Segment sent to Network Layer")
        self.send_segment(dst_ip, ack_segment, network)

    def send_segment(self, dst_ip, segment, network):
        packet = Packet(
            src_ip=self.ip,
            dst_ip=dst_ip,
            ttl=DEFAULT_TTL,
            protocol=IP_PROTOCOL_UDP,
            payload=segment
        )

        print(f"{self.name}: Layer 3: Segment received from Transport Layer: SRC_IP={self.ip}, DST_IP={dst_ip}, TTL={DEFAULT_TTL}")
        print(f"{self.name}: Layer 3: Destination IP read: {dst_ip}")
        print(f"{self.name}: Layer 3: Routing table lookup performed")

        dst_network = get_network_for_ip(dst_ip)

        route = self.routing_table.get(dst_network)

        if route is None:
            print(f"{self.name}: Layer 3: No route found. Packet dropped.")
            return

        next_hop_ip = route["next_hop"]

        print(f"{self.name}: Layer 3: Next-hop IP determined: {next_hop_ip}")
        print(f"{self.name}: Layer 3: Outgoing interface selected")
        print(f"{self.name}: Layer 3: Packet forwarded to Data Link Layer")

        #layer 2
        print(f"{self.name}: Layer 2: Packet received from Network Layer")

        dst_mac = self.mac_table.get(next_hop_ip)

        if dst_mac is None:
            print(f"{self.name}: Layer 2: Destination MAC not found. Frame dropped.")
            return

        print(f"{self.name}: Layer 2: Destination MAC lookup for next-hop IP ({next_hop_ip}) → {dst_mac}")

        frame = Frame(
            dst_mac=dst_mac,
            src_mac=self.mac,
            eth_type=ETH_TYPE_IPV4,
            payload=packet
        )

        print(f"{self.name}: Layer 2: Frame created: SRC_MAC={self.mac}, DST_MAC={dst_mac}")
        print(f"{self.name}: Layer 2: Frame sent")

        if self.ip == HOST_A_IP:
            network["router"].receive_frame(frame, INTERFACE_1, network)

        elif self.ip == HOST_B_IP:
            network["router"].receive_frame(frame, INTERFACE_2, network)

    def receive_frame(self, frame, network):
        print(f"{self.name}: Layer 2: Frame received")
        # Check if frame is for this host
        if frame.dst_mac != self.mac:
            print(f"{self.name}: Layer 2: Frame not for this host. Frame dropped.")
            return
        #check eth_type
        if frame.eth_type != ETH_TYPE_IPV4:
            print(f"{self.name}: Layer 2: Unsupported eth_type. Frame dropped.")
            return

        self.learned_macs.add(frame.src_mac)
        print(f"{self.name}: Layer 2: Source MAC learned: {frame.src_mac}")

        print(f"{self.name}: Layer 2: Packet delivered to Network Layer")

        packet = frame.payload
        self.receive_packet(packet, network)

    def receive_packet(self, packet, network):
        
        print(f"{self.name}: Layer 3: Packet received from Data Link Layer: SRC_IP={packet.src_ip}, DST_IP={packet.dst_ip}, TTL={packet.ttl}")
        print(f"{self.name}: Layer 3: Destination IP read: {packet.dst_ip}")

        if packet.dst_ip == self.ip:
            print(f"{self.name}: Layer 3: Packet identified as local delivery")
            print(f"{self.name}: Layer 3: Segment delivered to Transport Layer")

            segment = packet.payload
            self.receive_segment(segment, packet.src_ip, network)

        else:
            print(f"{self.name}: Layer 3: Packet not for this host. Packet dropped.")



class Router:
    def __init__(self, name):
        self.name = name
        self.routing_table = ROUTER_R1_ROUTING_TABLE
        self.mac_table = ROUTER_R1_MAC_TABLE

        self.interfaces = {
            INTERFACE_1: {
                "ip": ROUTER_R1_INTERFACE_1_IP,
                "mac": ROUTER_R1_INTERFACE_1_MAC
            },
            INTERFACE_2: {
                "ip": ROUTER_R1_INTERFACE_2_IP,
                "mac": ROUTER_R1_INTERFACE_2_MAC
            }
        }

        self.learned_macs = {}

    def receive_frame(self, frame, incoming_interface, network):
        
        print(f"{self.name}: Layer 2: Frame received on {incoming_interface}")

        interface_mac = self.interfaces[incoming_interface]["mac"]
        # Check if frame is for this router
        if frame.dst_mac != interface_mac:
            print(f"{self.name}: Layer 2: Frame not for this interface. Frame dropped.")
            return
        #check eth_type
        if frame.eth_type != ETH_TYPE_IPV4:
            print(f"{self.name}: Layer 2: Unsupported eth_type. Frame dropped.")
            return
        
        self.learned_macs[frame.src_mac] = incoming_interface
        print(f"{self.name}: Layer 2: Source MAC learned: {frame.src_mac} on {incoming_interface}")

        print(f"{self.name}: Layer 2: Packet delivered to Network Layer")

        packet = frame.payload
        self.forward_packet(packet, network)

    def forward_packet(self, packet, network):

        # Layer 3: receive packet from Layer 2
        print(f"{self.name}: Layer 3: Packet received from Data Link Layer: SRC_IP={packet.src_ip}, DST_IP={packet.dst_ip}, TTL={packet.ttl}")
        print(f"{self.name}: Layer 3: Destination IP read: {packet.dst_ip}")

        # TTL decreases at each router
        old_ttl = packet.ttl
        packet.decrement_ttl()
        print(f"{self.name}: Layer 3: TTL decremented: {old_ttl} → {packet.ttl}")

        # Drop packet
        if packet.ttl <= 0:
            print(f"{self.name}: Layer 3: Packet dropped due to TTL expiry")
            return

        print(f"{self.name}: Layer 3: Routing table lookup performed")

        dst_network = get_network_for_ip(packet.dst_ip)
        route = self.routing_table.get(dst_network)

        if route is None:
            print(f"{self.name}: Layer 3: No route found. Packet dropped.")
            return

        outgoing_interface = route["interface"]

        if route["next_hop"] is None:
            next_hop_ip = packet.dst_ip
        else:
            next_hop_ip = route["next_hop"]

        print(f"{self.name}: Layer 3: Next-hop IP determined: {next_hop_ip}")
        print(f"{self.name}: Layer 3: Outgoing interface selected ({outgoing_interface})")
        print(f"{self.name}: Layer 3: Packet forwarded to Data Link Layer")

        # create a new frame
        print(f"{self.name}: Layer 2: Packet received from Network Layer")

        dst_mac = self.mac_table.get(next_hop_ip)

        if dst_mac is None:
            print(f"{self.name}: Layer 2: Destination MAC not found. Frame dropped.")
            return

        print(f"{self.name}: Layer 2: Destination MAC lookup for next-hop IP ({next_hop_ip}) → {dst_mac}")

        src_mac = self.interfaces[outgoing_interface]["mac"]

        frame = Frame(
            dst_mac=dst_mac,
            src_mac=src_mac,
            eth_type=ETH_TYPE_IPV4,
            payload=packet
        )

        print(f"{self.name}: Layer 2: Frame created: SRC_MAC={src_mac}, DST_MAC={dst_mac}")

        if outgoing_interface == INTERFACE_1:
            print(f"{self.name}: Layer 2: Frame forwarded on Interface 1")
            network["host_a"].receive_frame(frame, network)

        elif outgoing_interface == INTERFACE_2:
            print(f"{self.name}: Layer 2: Frame forwarded on Interface 2")
            network["host_b"].receive_frame(frame, network)