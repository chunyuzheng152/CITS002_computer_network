# CITS3002_computer_network
chunyu_zheng 24279373


Mini Internet Protocol Stack Simulator

Overview
It simulates how data is sent from A to B through Router R1 using layer 2, layer 3, layer 4.


Host A 10.0.1.10
R1 interface 1 10.0.1.1
R1 interface 2 10.0.2.1
Host B 10.0.2.20

main.py: starts the simulation.
config.py: stores fixed IP, MAC, and constants.
protocol.py: stores Segment, Packet, and Frame classes.
devices.py: stores Host and Router classes.
README.md: explains the project.

Run the program form the project root diectory
  python main.py 10/100<message_size>

The maximum data size for one udp_like segment is 500 bytes.
If the message size is larger than 500 bytes, the message is split into multiple segments and sent sequentially.

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

###



Output
The program prints logs for each layer.
The logs show the process of encapsulation, routing, forwarding, MAC address lookup, TTL decrement, checksum verification, ACK transmission, and data delivery.


Assumptions
There is no real packet loss.
There is no real frame corruption.
All transmissions are deterministic.
Only Python standard libraries are used.
No socket or external networking library is used.