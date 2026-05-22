# CITS3002_computer_network
# Mini Internet Protocol Stack Simulator

#group members
chunyu_zheng 24279373
Fubin Qiu 23673779


Mini Internet Protocol Stack Simulator

Overview
It simulates how data is sent from A to B through Router R1 using layer 2, layer 3, layer 4.


## Network Topology

### IP Addresses

- Host A: 10.0.1.10
- Router R1 Interface 1: 10.0.1.1
- Router R1 Interface 2: 10.0.2.1
- Host B: 10.0.2.20

### MAC Addresses

- Host A: AA:AA:AA:AA:AA:AA
- Router R1 Interface 1: BB:BB:BB:BB:BB:BB
- Router R1 Interface 2: CC:CC:CC:CC:CC:CC
- Host B: DD:DD:DD:DD:DD:DD

main.py: starts the simulation.
config.py: stores fixed IP, MAC, and constants.
protocol.py: stores Segment, Packet, and Frame classes.
devices.py: stores Host and Router classes.
README.md: explains the project.

# Run the program form the project root diectory
  python main.py <message_size>
  such as 
  python main.py 10
  python main.py 500
  python main.py 501
  python main.py 1000


The maximum data size for one udp_like segment is 500 bytes.
If the message size is larger than 500 bytes, the message is split into multiple segments and sent sequentially.

## Requirements

- Python 3
- No external libraries are required.
- Only Python standard libraries are used.
- Networking libraries such as socket are not used.

Layer 2:Data Link Layer
Layer 2 uses an Ethernet-like frame.
The Frame class stores the Layer 2 header fields, including destination MAC address, source MAC address, type, and payload.
The payload of the frame is a layer 3 packet
 Layer 2 is responsible for frame creation, MAC address lookup, MAC learning, frame forwarding, and delivering the packet to Layer 3. 
The receiver checks the destination MAC address and Ethernet type before passing the packet to Layer 3. Invalid frames are dropped.


Layer 3:Network Layer
Layer 3 uses an IP-like packet.
The Packet class stores the source IP, destination IP, TTL, protocol, total length, and payload.
The payload is a Layer 4 segment. When the packet passes through Router R1, the TTL is decreased by 1.
Layer 3 is used for IP addressing, routing, forwarding, and delivering the segment to Layer 4 at the destination host.
Router R1 performs routing table lookup and selects the outgoing interface before forwarding the packet.

Layer 4:Transport Layer
Layer 4 uses a UDP-like segment with ACK support
The Segment class stores the Layer 4 header fields, including source port, destination port, length, checksum, type (0 for DATA, 1 for ACK), sequence number (0 or 1), and the application data
Layer 4 is responsible for port-based delivery, segmentation, error detection, and reliable data transfer

Key functionalities implemented include:
Segmentation: The maximum data size for a segment is limited to 500 bytes. If the application message exceeds this limit, it is segmented into multiple chunks.
Reliable Data Transfer (rdt2.2): The transport layer implements the rdt2.2 Alternating-Bit Protocol. The sender alternates sequence numbers between 0 and 1 for each DATA segment. 
Error Detection: A checksum is computed for each segment before transmission. The receiver verifies this checksum and discards the segment if it is corrupted.
ACK & Retransmission: Upon receiving a valid DATA segment, the receiver delivers it to the application and sends an ACK with the corresponding sequence number. If a segment is corrupted or is a duplicate, the receiver re-sends the last ACK. The sender waits for the correct ACK and will retransmit the current segment if an incorrect or duplicate ACK is received.




## Output and Logging

The program prints logs for each layer.

- Layer 2 frame creation, MAC address lookup, MAC learning, frame forwarding, and delivery to Layer 3.
- Layer 3 packet creation, routing table lookup, next-hop decision, TTL decrement, and delivery to Layer 4.
- Layer 4 segmentation, checksum computation, checksum verification, DATA segment transmission, ACK transmission, and retransmission handling.